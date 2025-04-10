"""
Command-line interface for the Stack Upgrade Analyzer.
"""

import os
import sys
import click
from pathlib import Path

from .upgrade_analyzer import analyze_changes, get_changes, get_changes_file_path

@click.group()
def main():
    """Stack Upgrade Analyzer - Analyze code compatibility issues when upgrading technology stacks."""
    pass

@main.command(name="get-changes")
@click.argument("stack", type=str)
@click.argument("current_version", type=str)
@click.argument("upgrade_version", type=str)
@click.option("--force", is_flag=True, default=False, help="Force regeneration of changes file")
def get_changes_cmd(stack, current_version, upgrade_version, force):
    """
    Fetch breaking changes between versions.
    
    STACK: Technology stack (e.g., node, java, python)
    
    CURRENT_VERSION: Current version
    
    UPGRADE_VERSION: Target upgrade version
    """
    try:
        print(f"Fetching breaking changes for {stack} {current_version} → {upgrade_version}...")
        get_changes(stack, current_version, upgrade_version, force)
        
        # Check if the changes file was created
        changes_file = get_changes_file_path(stack, current_version, upgrade_version)
        
        if changes_file.exists():
            print(f"Changes file created successfully at: {changes_file}")
            print("First 10 lines of the changes file:")
            with open(changes_file, 'r') as f:
                for i, line in enumerate(f):
                    if i < 10:
                        print(line.rstrip())
                    else:
                        break
        else:
            print(f"Error: Failed to create changes file at {changes_file}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

@main.command(name="analyze-changes")
@click.argument("changes_file", type=str)
@click.argument("directory", type=str)
@click.option("--output", type=str, help="Output file path")
@click.option("--stack", type=str, default="node", help="Technology stack (e.g., node, java, python)")
def analyze_changes_cmd(changes_file, directory, output, stack):
    """
    Analyze codebase for compatibility issues.
    
    CHANGES_FILE: Path to the changes file
    
    DIRECTORY: Directory to analyze
    """
    try:
        print(f"Analyzing codebase at {directory} using changes file {changes_file}...")
        analyze_changes(changes_file, directory, output, stack)
        print("Analysis completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

# This ensures the CLI is properly executed when run directly
if __name__ == '__main__':
    main()
