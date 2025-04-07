#!/usr/bin/env python
import os
import sys
import subprocess
import click
import logging
from typing import Optional
import hashlib
import shutil
from pathlib import Path
from lark import exceptions

def configure_logging(verbose=False):
    """Configure logging levels based on verbosity"""
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    else:
        # Suppress debug messages from dependencies
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        # Suppress verbose output from dependencies
        for logger_name in [
            'graphviz', 'matplotlib', 'tensorflow', 'jax',
            'pydot', 'PIL', 'torch', 'urllib3', 'requests',
            'filelock', 'numba', 'h5py', 'asyncio', 'parso',
            'matplotlib.font_manager', 'matplotlib.ticker'
        ]:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from neural.parser.parser import create_parser, ModelTransformer, DSLValidationError
from neural.code_generation.code_generator import generate_code
from neural.shape_propagation.shape_propagator import ShapePropagator
from neural.dashboard.tensor_flow import create_animated_network
from neural.hpo.hpo import optimize_and_return
from neural.code_generation.code_generator import generate_optimized_dsl

# Create logger for this module
logger = logging.getLogger(__name__)

# Supported datasets (extend as implemented)
SUPPORTED_DATASETS = {"MNIST", "CIFAR10", "CIFAR100", "ImageNet"}

# Global CLI context for shared options
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose: bool):
    """Neural CLI: A compiler-like interface for .neural and .nr files."""
    configure_logging(verbose)
    logger.debug("Verbose mode enabled")

# Compile command
@cli.command()
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--backend', '-b', default='tensorflow', help='Target backend', type=click.Choice(['tensorflow', 'pytorch', 'onnx'], case_sensitive=False))
@click.option('--dataset', default='MNIST', help='Dataset name (e.g., MNIST, CIFAR10)')
@click.option('--output', '-o', default=None, help='Output file path (defaults to <file>_<backend>.py)')
@click.option('--dry-run', is_flag=True, help='Preview generated code without writing to file')
@click.option('--hpo', is_flag=True, help='Enable hyperparameter optimization')
def compile(file: str, backend: str, dataset: str, output: Optional[str], dry_run: bool, hpo: bool):
    """Compile a .neural or .nr file into an executable Python script.

    Example: neural compile my_model.neural --backend pytorch --output model.py --hpo
    """
    ext = os.path.splitext(file)[1].lower()
    start_rule = 'network' if ext in ['.neural', '.nr'] else 'research' if ext == '.rnr' else None
    if not start_rule:
        logger.error(f"Unsupported file type: {ext}. Use .neural, .nr, or .rnr")
        sys.exit(1)

    logger.info(f"Compiling {file} for {backend} backend")
    parser_instance = create_parser(start_rule=start_rule)
    with open(file, 'r') as f:
        content = f.read()

    try:
        tree = parser_instance.parse(content)
        model_data = ModelTransformer().transform(tree)
    except (exceptions.UnexpectedCharacters, exceptions.UnexpectedToken, DSLValidationError) as e:
        logger.error(f"Parsing/transforming {file} failed: {e}")
        sys.exit(1)

    if hpo:
        logger.debug("Running HPO for %s", file)
        if dataset not in SUPPORTED_DATASETS:
            logger.warning("Dataset '%s' may not be supported. Supported: %s", dataset, SUPPORTED_DATASETS)
        best_params = optimize_and_return(content, n_trials=3, dataset_name=dataset, backend=backend)
        logger.info("Best parameters: %s", best_params)
        content = generate_optimized_dsl(content, best_params)

    try:
        code = generate_code(model_data, backend)
    except Exception as e:
        logger.error(f"Code generation failed: {e}")
        sys.exit(1)

    output_file = output or f"{os.path.splitext(file)[0]}_{backend}.py"
    if dry_run:
        click.echo("Generated code (dry run):\n" + code)
    else:
        with open(output_file, 'w') as f:
            f.write(code)
        logger.info(f"Compiled {file} to {output_file}")
        click.echo(f"Output written to {output_file}")

# Run command
@cli.command()
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--backend', '-b', default='tensorflow', help='Backend to run', type=click.Choice(['tensorflow', 'pytorch'], case_sensitive=False))
@click.option('--dataset', default='MNIST', help='Dataset name (e.g., MNIST, CIFAR10)')
@click.option('--hpo', is_flag=True, help='Enable HPO for .neural files')
def run(file: str, backend: str, dataset: str, hpo: bool):
    ext = os.path.splitext(file)[1].lower()
    if ext == '.py':
        logger.info(f"Running {file} with {backend} backend")
        try:
            subprocess.run([sys.executable, file], check=True)
            logger.info("Execution completed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Execution failed with exit code {e.returncode}")
            sys.exit(e.returncode)
    elif ext in ['.neural', '.nr'] and hpo:
        logger.info(f"Optimizing and running {file} with {backend} backend")
        start_rule = 'network' if ext in ['.neural', '.nr'] else None
        if not start_rule:
            logger.error(f"Unsupported file type for HPO: {ext}")
            sys.exit(1)

        with open(file, 'r') as f:
            content = f.read()

        if dataset not in SUPPORTED_DATASETS:
            logger.warning("Dataset '%s' may not be supported. Supported: %s", dataset, SUPPORTED_DATASETS)

        # Optimize and generate code
        best_params = optimize_and_return(content, n_trials=3, dataset_name=dataset, backend=backend)
        logger.info("Best parameters found: %s", best_params)
        optimized_config = generate_optimized_dsl(content, best_params)

        output_file = f"{os.path.splitext(file)[0]}_optimized_{backend}.py"
        parser_instance = create_parser(start_rule=start_rule)
        try:
            tree = parser_instance.parse(optimized_config)
            model_data = ModelTransformer().transform(tree)
            code = generate_code(model_data, backend, best_params=best_params)
            with open(output_file, 'w') as f:
                f.write(code)
            logger.info(f"Compiled optimized {file} to {output_file}")
        except Exception as e:
            logger.error(f"Optimization or code generation failed: {e}")
            sys.exit(1)

        # Run the compiled file
        try:
            subprocess.run([sys.executable, output_file], check=True)
            logger.info("Execution completed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Execution failed with exit code {e.returncode}")
            sys.exit(e.returncode)
    else:
        logger.error(f"Expected a .py file, got {ext}. Use 'compile' first or add --hpo for .neural files.")
        sys.exit(1)

# Visualize command
@cli.command()
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--format', '-f', default='html', help='Output format', type=click.Choice(['html', 'png', 'svg'], case_sensitive=False))
@click.option('--cache/--no-cache', default=True, help='Use cached visualizations if available')
def visualize(file: str, format: str, cache: bool):
    """Visualize network architecture and shape propagation.

    Example: neural visualize my_model.neural --format png --no-cache
    """
    logger.info(f"Visualizing {file} in {format} format")
    ext = os.path.splitext(file)[1].lower()
    start_rule = 'network' if ext in ['.neural', '.nr'] else 'research' if ext == '.rnr' else None
    if not start_rule:
        logger.error(f"Unsupported file type: {ext}")
        sys.exit(1)

    cache_dir = Path(".neural_cache")
    cache_dir.mkdir(exist_ok=True)
    file_hash = hashlib.sha256(Path(file).read_bytes()).hexdigest()
    cache_file = cache_dir / f"viz_{file_hash}_{format}"

    if cache and cache_file.exists():
        logger.info(f"Using cached visualization: {cache_file}")
        shutil.copy(cache_file, f"architecture.{format}")
        click.echo(f"Cached visualization copied to architecture.{format}")
        return

    parser_instance = create_parser(start_rule=start_rule)
    with open(file, 'r') as f:
        content = f.read()

    try:
        tree = parser_instance.parse(content)
        model_data = ModelTransformer().transform(tree)
    except Exception as e:
        logger.error(f"Processing {file} failed: {e}")
        sys.exit(1)

    propagator = ShapePropagator()
    input_shape = model_data['input']['shape']
    if not input_shape:
        logger.error("Input shape not defined in model")
        sys.exit(1)

    shape_history = []
    with click.progressbar(model_data['layers'], label="Propagating shapes") as bar:
        for layer in bar:
            input_shape = propagator.propagate(input_shape, layer, model_data.get('framework', 'tensorflow'))
            shape_history.append({"layer": layer['type'], "output_shape": input_shape})

    report = propagator.generate_report()
    dot = report['dot_graph']
    dot.format = format if format != 'html' else 'svg'
    dot.render('architecture', cleanup=True)

    if format == 'html':
        report['plotly_chart'].write_html('shape_propagation.html')
        create_animated_network(shape_history).write_html('tensor_flow.html')
        click.echo("""
        Visualizations generated:
        - architecture.svg (Network architecture)
        - shape_propagation.html (Parameter count chart)
        - tensor_flow.html (Data flow animation)
        """)
    else:
        click.echo(f"Visualization saved as architecture.{format}")

    if cache:
        shutil.copy(f"architecture.{format}", cache_file)
        logger.debug(f"Cached visualization at {cache_file}")

# Clean command
@cli.command()
def clean():
    """Remove generated files (e.g., .py, .png, .svg, .html, cache)."""
    extensions = ['.py', '.png', '.svg', '.html']
    removed = False
    for file in os.listdir('.'):
        if any(file.endswith(ext) for ext in extensions):
            os.remove(file)
            logger.info(f"Removed {file}")
            removed = True
    if os.path.exists(".neural_cache"):
        shutil.rmtree(".neural_cache")
        logger.info("Removed cache directory")
        removed = True
    if not removed:
        click.echo("No files to clean")

# Version command
@cli.command()
def version():
    """Show the version of Neural CLI and dependencies."""
    import lark
    click.echo("Neural CLI v0.1.0")  # Update with your actual version
    click.echo(f"Python: {sys.version.split()[0]}")
    click.echo(f"Click: {click.__version__}")
    click.echo(f"Lark: {lark.__version__}")
    for pkg in ('torch', 'tensorflow', 'optuna'):
        try:
            ver = __import__(pkg).__version__
            click.echo(f"{pkg.capitalize()}: {ver}")
        except ImportError:
            click.echo(f"{pkg.capitalize()}: Not installed")

# Debug command
@cli.command()
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--gradients', is_flag=True, help='Analyze gradient flow')
@click.option('--dead-neurons', is_flag=True, help='Detect dead neurons')
@click.option('--anomalies', is_flag=True, help='Detect training anomalies')
@click.option('--step', is_flag=True, help='Enable step debugging mode')
@click.option('--backend', '-b', default='tensorflow', help='Backend for runtime', type=click.Choice(['tensorflow', 'pytorch'], case_sensitive=False))
@click.option('--dataset', default='MNIST', help='Dataset name (e.g., MNIST, CIFAR10)')
def debug(file: str, gradients: bool, dead_neurons: bool, anomalies: bool, step: bool, backend: str, dataset: str):
    """Debug a neural network model with NeuralDbg.

    Example: neural debug my_model.neural --gradients --step --backend pytorch
    """
    logger.info(f"Debugging {file} with NeuralDbg (backend: {backend})")
    ext = os.path.splitext(file)[1].lower()
    start_rule = 'network' if ext in ['.neural', '.nr'] else 'research' if ext == '.rnr' else None
    if not start_rule:
        logger.error(f"Unsupported file type: {ext}")
        sys.exit(1)

    if dataset not in SUPPORTED_DATASETS:
        logger.warning("Dataset '%s' may not be supported. Supported: %s", dataset, SUPPORTED_DATASETS)

    parser_instance = create_parser(start_rule=start_rule)
    with open(file, 'r') as f:
        content = f.read()

    try:
        tree = parser_instance.parse(content)
        model_data = ModelTransformer().transform(tree)
    except Exception as e:
        logger.error(f"Processing {file} failed: {e}")
        sys.exit(1)

    # Shape propagation for baseline
    propagator = ShapePropagator(debug=True)
    input_shape = model_data['input']['shape']
    for layer in model_data['layers']:
        input_shape = propagator.propagate(input_shape, layer, backend)
    trace_data = propagator.get_trace()

    # Debugging modes
    if gradients:
        logger.info("Gradient flow analysis not fully implemented yet (requires runtime)")
        click.echo("Gradient flow trace (simulated):")
        for entry in trace_data:
            click.echo(f"Layer {entry['layer']}: mean_activation = {entry.get('mean_activation', 'N/A')}")
    if dead_neurons:
        logger.info("Dead neuron detection not fully implemented yet (requires runtime)")
        click.echo("Dead neuron trace (simulated):")
        for entry in trace_data:
            click.echo(f"Layer {entry['layer']}: active_ratio = {entry.get('active_ratio', 'N/A')}")
    if anomalies:
        logger.info("Anomaly detection not fully implemented yet (requires runtime)")
        click.echo("Anomaly trace (simulated):")
        for entry in trace_data:
            if 'anomaly' in entry:
                click.echo(f"Layer {entry['layer']}: {entry['anomaly']}")
    if step:
        logger.info("Step debugging mode")
        for i, layer in enumerate(model_data['layers']):
            input_shape = propagator.propagate(input_shape, layer, backend)
            click.echo(f"Step {i+1}: {layer['type']} - Output Shape: {input_shape}")
            if click.confirm("Continue?", default=True):
                continue
            else:
                logger.info("Debugging paused by user")
                break

    click.echo("Debug session completed. Full runtime debugging coming soon!")

# No-code command
@cli.command(name='no-code')
@click.option('--port', default=8051, help='Web interface port', type=int)
def no_code(port: int):
    """Launch the no-code interface for building models.

    Example: neural no-code --port 8051
    """
    from neural.dashboard.dashboard import app  # Assuming a dashboard module exists
    logger.info("Launching no-code interface at http://localhost:%s", port)
    try:
        app.run_server(debug=False, host="localhost", port=port)
    except Exception as e:
        logger.error(f"Failed to launch no-code interface: {e}")
        sys.exit(1)

# Remove standalone HPO command (integrated into run/compile)
# If you want to keep it separate, uncomment and adjust:
# @cli.command()
# @click.argument('file')
# @click.option('--n-trials', default=20)
# @click.option('--dataset', default='MNIST')
# def hpo(file, n_trials, dataset):
#     """Run hyperparameter optimization"""
#     with open(file) as f:
#         config = f.read()
#     best_params = optimize_and_return(config, n_trials, dataset)
#     click.echo(f"Best parameters: {best_params}")

if __name__ == '__main__':
    cli()