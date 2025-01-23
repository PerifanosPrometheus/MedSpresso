"""Command line interface for MedSpresso."""
import click
from pathlib import Path
import yaml
from rich.console import Console
import json
from typing import Optional
from .ollama import OllamaClient
from .model_configs import get_model_config, list_supported_models

console = Console()

# Configuration
DEFAULT_PROMPTS_FILE = Path("prompts/extraction_prompts.yaml")

def get_available_prompt_types(prompts_file: Path = DEFAULT_PROMPTS_FILE) -> list[str]:
    """Get available prompt types from the prompts YAML file"""
    try:
        with open(prompts_file) as f:
            prompts = yaml.safe_load(f)
            return list(prompts.keys())
    except Exception as e:
        console.print(f"[red]Error loading prompts file:[/red] {e}")
        return ['medications']

@click.group()
def cli():
    """MedSpresso CLI - Extract information from clinical text using LLMs"""
    pass

@cli.command()
def list_models():
    """List available models"""
    console.print("\n[bold]Available Models:[/bold]")
    for model_name in list_supported_models():
        config = get_model_config(model_name)
        console.print(f"\n[cyan]{model_name}[/cyan]")
        console.print(f"Description: {config.get('description', 'N/A')}")
        if tags := config.get('tags'):
            console.print(f"Tags: {', '.join(tags)}")

@cli.command()
@click.option(
    '--input',
    'input_file',
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help='Input file containing clinical text'
)
@click.option(
    '--model',
    type=click.Choice(list_supported_models()),
    default='deepseek-r1:1.5b',
    help='Model to use for extraction'
)
@click.option(
    '--prompt-type',
    type=click.Choice(get_available_prompt_types()),
    default='medications',
    help='Type of extraction to perform'
)
@click.option(
    '--format',
    'output_format',
    type=click.Choice(['text', 'json']),
    default='text',
    help='Output format'
)
@click.option(
    '--output',
    'output_file',
    type=click.Path(path_type=Path),
    help='Output file path (optional, will print to console if not specified)'
)
def extract(
    input_file: Path,
    model: str,
    prompt_type: str,
    output_format: str,
    output_file: Optional[Path],
):
    """Extract information from clinical text"""
    try:
        # Initialize Ollama client
        client = OllamaClient(model)
        
        with console.status("[bold green]Loading prompt template..."):
            # Load prompt template
            with open(DEFAULT_PROMPTS_FILE) as f:
                prompts = yaml.safe_load(f)
                if prompt_type not in prompts:
                    raise click.BadParameter(f"Prompt type '{prompt_type}' not found in prompts file")
                prompt_template = prompts[prompt_type]

            # Read input text
            with open(input_file) as f:
                text = f.read().strip()

            # Create the prompt
            prompt = prompt_template.format(text=text)

        # Run inference
        with console.status("[bold green]Running inference...") as status:
            result = []
            for chunk in client.generate(prompt):
                result.append(chunk)
                console.print(chunk, end='')
            
            final_result = ''.join(result)
            
            # Handle output
            if output_file:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(final_result)
                console.print(f"\n[green]Results written to:[/green] {output_file}")
            else:
                console.print("\n[bold]Results:[/bold]")
                console.print("─" * 40)
                console.print(final_result)
                console.print("─" * 40)

    except Exception as e:
        console.print(f"[red]Error during extraction:[/red] {e}")
        raise click.Abort()

if __name__ == '__main__':
    cli() 