#!/usr/bin/env python
"""
Main entry point for Bolor CLI.

This module handles command-line arguments and dispatches to the appropriate functionality.
"""

import os
import sys
import warnings
import typer
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich import print as rprint

# Suppress dependency warnings from requests library
warnings.filterwarnings("ignore", category=Warning)

from bolor.utils.config import Config
from bolor.agent.scanner import Scanner
from bolor.agent.fixer import Fixer
from bolor.agent.planner import Planner
from bolor.agent.generator import Generator
from bolor.agent.dataset_loader import DatasetLoader

# Initialize typer app and console
app = typer.Typer(
    help="Bolor: Local LLM-based code repair tool with self-healing capabilities.",
    add_completion=False,
)
console = Console()


@app.command()
def scan(
    project_path: str = typer.Argument(
        ".", help="Path to the project to scan"
    ),
    fix: bool = typer.Option(
        False, "--fix", "-f", help="Automatically apply fixes for detected issues"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Scan a codebase for issues and optionally fix them.
    """
    console.print(f"[bold blue]Scanning project: {project_path}[/bold blue]")
    
    # Initialize components
    config = Config()
    config.set("verbose", verbose)
    scanner = Scanner(config)
    
    # Scan for issues
    try:
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            console.print(f"[bold red]Error: Project path {project_path} does not exist[/bold red]")
            return 1
        
        issues = scanner.scan_directory(project_path)
        if not issues:
            console.print("[green]No issues found![/green]")
            return 0
        
        console.print(f"[yellow]Found {len(issues)} potential issues[/yellow]")
        for i, issue in enumerate(issues, 1):
            console.print(f"[yellow]Issue {i}:[/yellow] {issue.description}")
            console.print(f"  [dim]File:[/dim] {issue.file_path}:{issue.line_number}")
            if verbose:
                console.print(f"  [dim]Code:[/dim] {issue.code_snippet}")
        
        # Apply fixes if requested
        if fix:
            console.print("\n[bold blue]Applying fixes...[/bold blue]")
            fixer = Fixer(config)
            fixed_issues = fixer.fix_issues(issues)
            
            console.print(f"[green]Successfully fixed {len(fixed_issues)} issues[/green]")
            for i, issue in enumerate(fixed_issues, 1):
                console.print(f"[green]Fix {i}:[/green] {issue.description}")
                console.print(f"  [dim]File:[/dim] {issue.file_path}:{issue.line_number}")
                if verbose:
                    console.print(f"  [dim]Before:[/dim] {issue.code_snippet}")
                    console.print(f"  [dim]After:[/dim] {issue.fixed_code_snippet}")
        
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error during scan: {str(e)}[/bold red]")
        if verbose:
            console.print_exception()
        return 1


@app.command()
def plan(
    project_path: str = typer.Argument(
        ".", help="Path to the project to analyze"
    ),
    output_format: str = typer.Option(
        "text", "--format", "-f", help="Output format: text, markdown, or json"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Analyze a codebase and suggest improvements.
    """
    console.print(f"[bold blue]Planning improvements for: {project_path}[/bold blue]")
    
    # Initialize components
    config = Config()
    config.set("verbose", verbose)
    config.set("output_format", output_format)
    planner = Planner(config)
    
    # Analyze project
    try:
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            console.print(f"[bold red]Error: Project path {project_path} does not exist[/bold red]")
            return 1
        
        suggestions = planner.analyze_project(project_path)
        if not suggestions:
            console.print("[green]No improvement suggestions found.[/green]")
            return 0
        
        console.print(f"[green]Found {len(suggestions)} improvement suggestions:[/green]")
        for i, suggestion in enumerate(suggestions, 1):
            console.print(f"[green]Suggestion {i}:[/green] {suggestion.title}")
            console.print(f"  [dim]Type:[/dim] {suggestion.type}")
            console.print(f"  [dim]Description:[/dim] {suggestion.description}")
            if verbose and suggestion.code_example:
                console.print(f"  [dim]Example:[/dim]\n{suggestion.code_example}")
        
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error during planning: {str(e)}[/bold red]")
        if verbose:
            console.print_exception()
        return 1


@app.command()
def deploy_check(
    project_path: str = typer.Argument(
        ".", help="Path to the project to check"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Check a codebase for deployment issues.
    """
    console.print(f"[bold blue]Checking deployment for: {project_path}[/bold blue]")
    
    # Initialize components
    config = Config()
    config.set("verbose", verbose)
    scanner = Scanner(config)
    
    # Check for deployment issues
    try:
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            console.print(f"[bold red]Error: Project path {project_path} does not exist[/bold red]")
            return 1
        
        issues = scanner.scan_ci_config(project_path)
        if not issues:
            console.print("[green]No deployment issues found![/green]")
            return 0
        
        console.print(f"[yellow]Found {len(issues)} potential deployment issues:[/yellow]")
        for i, issue in enumerate(issues, 1):
            console.print(f"[yellow]Issue {i}:[/yellow] {issue.description}")
            console.print(f"  [dim]File:[/dim] {issue.file_path}")
            if verbose:
                console.print(f"  [dim]Details:[/dim] {issue.details}")
        
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error during deployment check: {str(e)}[/bold red]")
        if verbose:
            console.print_exception()
        return 1


@app.command()
def download_resources(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force re-download of resources"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Download models and datasets for Bolor.
    """
    console.print("[bold blue]Downloading resources for Bolor...[/bold blue]")
    
    # Initialize components
    config = Config()
    config.set("verbose", verbose)
    config.set("force_download", force)
    dataset_loader = DatasetLoader(config)
    
    # Download resources
    try:
        # Download and prepare model
        console.print("[blue]Downloading model...[/blue]")
        model_path = dataset_loader.download_model(force=force)
        console.print(f"[green]Model downloaded to: {model_path}[/green]")
        
        # Download and prepare datasets
        console.print("[blue]Downloading datasets...[/blue]")
        dataset_paths = dataset_loader.download_datasets(force=force)
        console.print(f"[green]Downloaded {len(dataset_paths)} datasets:[/green]")
        for name, path in dataset_paths.items():
            console.print(f"  [dim]{name}:[/dim] {path}")
        
        # Build vector store
        console.print("[blue]Building vector store...[/blue]")
        vector_store_path = dataset_loader.build_vector_store()
        console.print(f"[green]Vector store built at: {vector_store_path}[/green]")
        
        console.print("[bold green]All resources downloaded successfully![/bold green]")
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error downloading resources: {str(e)}[/bold red]")
        if verbose:
            console.print_exception()
        return 1


@app.command()
def generate(
    prompt: str = typer.Argument(
        ..., help="Natural language description of what to generate"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="File to save the generated code to"
    ),
    language: Optional[str] = typer.Option(
        None, "--language", "-l", help="Programming language to generate in (auto-detected if not specified)"
    ),
    no_comments: bool = typer.Option(
        False, "--no-comments", help="Generate code without explanatory comments"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Generate code from a natural language description.
    """
    console.print(f"[bold blue]Generating code for: {prompt}[/bold blue]")
    
    # Initialize components
    config = Config()
    config.set("verbose", verbose)
    generator = Generator(config)
    
    # Generate code
    try:
        generated_code = generator.generate_from_prompt(
            prompt=prompt, 
            language=language,
            add_comments=not no_comments
        )
        
        console.print(f"[green]Generated code:[/green]")
        console.print(generated_code)
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            
            # If directory doesn't exist, create it
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(generated_code)
            console.print(f"[green]Code saved to: {output_file}[/green]")
        
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error generating code: {str(e)}[/bold red]")
        if verbose:
            console.print_exception()
        return 1


# Default command handler for natural language interface
@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    prompt: Optional[str] = typer.Argument(
        None, help="Natural language prompt (if no command is specified)"
    ),
):
    """
    If no command is specified but a prompt is provided,
    treat it as a generate command.
    """
    # Only process if no command was specified but a prompt was provided
    if ctx.invoked_subcommand is None and prompt:
        # Call the generate command with the provided prompt
        return generate(prompt=prompt)


def preprocess_args():
    """
    Preprocesses command line arguments to handle quoted strings properly.
    Specifically fixes issues with the 'generate' command when using quotes.
    """
    # Commands that shouldn't be treated as generate prompts
    KNOWN_COMMANDS = {"scan", "plan", "deploy_check", "deploy-check", 
                     "download_resources", "download-resources", "generate"}
    
    if len(sys.argv) > 1:
        # Check if first argument is a known command
        cmd = sys.argv[1].replace("-", "_")  # normalize command name
        if cmd in KNOWN_COMMANDS:
            # This is a valid command, let Typer handle it normally
            return None
        
        # Special handling for generate command with quoted arguments
        if len(sys.argv) >= 3 and sys.argv[1] == "generate":
            # Extract the options
            options = {}
            i = 3
            while i < len(sys.argv):
                if sys.argv[i].startswith("--") or sys.argv[i].startswith("-"):
                    opt_name = sys.argv[i].lstrip("-")
                    if i + 1 < len(sys.argv) and not sys.argv[i+1].startswith("-"):
                        options[opt_name] = sys.argv[i+1]
                        i += 2
                    else:
                        options[opt_name] = True
                        i += 1
                else:
                    i += 1
            
            # Get the prompt
            prompt = sys.argv[2]
            
            # Extract specific options
            output_file = options.get("output") or options.get("o")
            language = options.get("language") or options.get("l")
            no_comments = "no-comments" in options
            verbose = "verbose" in options or "v" in options
            
            # Directly call generate with the proper arguments
            return generate(
                prompt=prompt,
                output_file=output_file,
                language=language,
                no_comments=no_comments,
                verbose=verbose
            )
    
    return None

def main():
    """
    Main entry point.
    """
    try:
        # Apply preprocessing first - only for special cases
        result = preprocess_args()
        
        # If preprocessing handled the command, return its result
        if result is not None:
            return result
            
        # Otherwise, proceed with normal command processing
        return app()
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")
        console.print_exception()
        return 1


if __name__ == "__main__":
    sys.exit(main())
