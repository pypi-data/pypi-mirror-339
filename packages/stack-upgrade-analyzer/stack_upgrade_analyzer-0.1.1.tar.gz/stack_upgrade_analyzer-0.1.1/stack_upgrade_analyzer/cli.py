"""
Command-line interface for the Stack Upgrade Analyzer.
"""

import os
import sys
import click
from pathlib import Path

from .upgrade_analyzer import analyze_changes, get_changes

@click.group()
def main():
    """Stack Upgrade Analyzer - Analyze code compatibility issues when upgrading technology stacks."""
    pass

@main.command()
@click.option('--stack', required=True, help='Technology stack (e.g., node, java, python)')
@click.option('--current-version', required=True, help='Current version')
@click.option('--upgrade-version', required=True, help='Target upgrade version')
@click.option('--force', is_flag=True, help='Force regeneration of changes file')
def get_changes_cmd(stack, current_version, upgrade_version, force):
    """Fetch breaking changes between versions."""
    get_changes(stack, current_version, upgrade_version, force)

@main.command()
@click.option('--changes-file', required=True, help='Path to the changes file')
@click.option('--dir', required=True, help='Directory to analyze')
@click.option('--output', help='Output file path')
@click.option('--stack', default='node', help='Technology stack (e.g., node, java, python)')
def analyze_changes_cmd(changes_file, dir, output, stack):
    """Analyze codebase for compatibility issues."""
    analyze_changes(changes_file, dir, output, stack)

if __name__ == '__main__':
    main()
