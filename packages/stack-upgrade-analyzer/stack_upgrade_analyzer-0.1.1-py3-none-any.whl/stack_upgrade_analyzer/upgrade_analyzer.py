#!/usr/bin/env python3
"""
Stack Upgrade Analyzer - Core functionality for analyzing code compatibility issues.
"""

import os
import sys
import json
import subprocess
import shutil
from typing import List, Tuple, Optional, Dict
from datetime import datetime
from pathlib import Path

# Import utility functions
from .utils import get_package_root, get_data_dir, get_changes_dir

# Import required packages
import requests
from dotenv import load_dotenv
import click
import inquirer

# Set up paths
BASE_DIR = get_package_root()
DATA_DIR = get_data_dir()
CHANGES_DIR = get_changes_dir()

# Stack-specific file extensions and exclusion paths
STACK_MAPPINGS = {
    "node": {
        "extensions": ["js", "jsx", "ts", "tsx"],
        "exclude_paths": ["node_modules", "dist", "build", ".git"]
    },
    "java": {
        "extensions": ["java", "kt", "scala"],
        "exclude_paths": ["target", "build", ".gradle", ".git"]
    },
    "python": {
        "extensions": ["py"],
        "exclude_paths": ["__pycache__", "venv", ".venv", "env", ".env", ".git"]
    },
    "ruby": {
        "extensions": ["rb"],
        "exclude_paths": ["vendor", ".bundle", ".git"]
    },
    "csharp": {
        "extensions": ["cs"],
        "exclude_paths": ["bin", "obj", "packages", ".git"]
    },
    "php": {
        "extensions": ["php"],
        "exclude_paths": ["vendor", ".git"]
    }
}

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
CHANGES_DIR.mkdir(exist_ok=True)

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")


def backup_config_file():
    """Create a backup of the config file if it exists."""
    config_file = BASE_DIR / ".env"
    if config_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = f"{config_file}.backup.{timestamp}"
        shutil.copy2(config_file, backup_path)
        print(f"Backup of existing configuration created at: {backup_path}")


def save_config(config: Dict[str, str]):
    """Save configuration to .env file."""
    with open(BASE_DIR / ".env", "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")


@click.group()
def cli():
    """Stack Upgrade Analyzer - Analyze compatibility between software versions."""
    # Create necessary directories
    DATA_DIR.mkdir(exist_ok=True)
    CHANGES_DIR.mkdir(exist_ok=True)


@cli.command()
def config():
    """Configure API keys and settings."""
    print("Stack Upgrade Analyzer Configuration")
    print("This will guide you through setting up the necessary API keys.\n")

    # Create a backup of the existing config file
    backup_config_file()

    # Load existing configuration
    load_dotenv(dotenv_path=BASE_DIR / ".env")
    
    # Prepare questions
    questions = [
        inquirer.Text('PERPLEXITY_API_KEY',
                     message="Enter your Perplexity API key",
                     default=os.environ.get('PERPLEXITY_API_KEY', '')),
        inquirer.Text('AWS_PROFILE',
                     message="Enter your AWS profile name for Bedrock access",
                     default=os.environ.get('AWS_PROFILE', 'default')),
        inquirer.Text('AWS_REGION',
                     message="Enter AWS region for Bedrock",
                     default=os.environ.get('AWS_REGION', 'us-east-1')),
        inquirer.Confirm('SAVE_REPORTS',
                        message="Save analysis reports for future reference?",
                        default=os.environ.get('SAVE_REPORTS', 'True').lower() in ('true', 'yes', 'y', '1')),
    ]
    
    try:
        answers = inquirer.prompt(questions)
        if answers:
            # Convert boolean to string
            if isinstance(answers['SAVE_REPORTS'], bool):
                answers['SAVE_REPORTS'] = str(answers['SAVE_REPORTS'])
            
            # Save configuration
            save_config(answers)
            print("Configuration saved successfully!")
            print(f"Configuration file: {BASE_DIR / '.env'}")
    except Exception as e:
        print(f"Error during configuration: {str(e)}")
        sys.exit(1)


def get_changes_file_path(stack: str, current_version: str, upgrade_version: str) -> Path:
    """Generate the path for the changes file."""
    stack_dir = CHANGES_DIR / stack
    stack_dir.mkdir(exist_ok=True)
    return stack_dir / f"{current_version}_{upgrade_version}_changes.md"


def fetch_changes_from_perplexity(stack: str, current_version: str, upgrade_version: str) -> str:
    """Fetch breaking changes from Perplexity API."""
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    if not api_key:
        raise ValueError("Perplexity API key not found. Run 'stack-upgrade-analyzer config' to set up your API keys.")
    
    try:
        # Create prompt for Perplexity
        prompt = f"""I need a comprehensive list of all breaking changes, deprecations, and API modifications when upgrading from {stack} {current_version} to {stack} {upgrade_version}.

Format the response as a detailed Markdown document with the following structure:
1. A brief summary of the major changes
2. Breaking changes organized by version (e.g., changes introduced in each intermediate version)
3. For each breaking change, include:
   - The specific API, method, or feature affected
   - What changed and why
   - How to migrate or update code to be compatible
   - Code examples showing before and after when possible

Be extremely thorough and include ALL breaking changes, no matter how minor. This will be used for automated compatibility analysis."""

        # Make API request to Perplexity
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides detailed information about breaking changes between Node.js versions. Be precise, technical, and comprehensive."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            },
            timeout=120
        )
        
        if not response.ok:
            raise ValueError(f"Perplexity API error ({response.status_code}): {response.text}")
        
        data = response.json()
        if not data.get("choices") or not data["choices"][0].get("message") or not data["choices"][0]["message"].get("content"):
            raise ValueError("Invalid response from Perplexity API")
        
        return data["choices"][0]["message"]["content"]
        
    except Exception as e:
        raise


@cli.command()
@click.option('--stack', required=True, help='Technology stack (e.g., node, python)')
@click.option('--current-version', required=True, help='Current version')
@click.option('--upgrade-version', required=True, help='Target upgrade version')
@click.option('--force', is_flag=True, help='Force regeneration of changes file')
def get_changes(stack: str, current_version: str, upgrade_version: str, force: bool):
    """Fetch breaking changes between versions."""
    # Normalize versions
    current_version = current_version.lstrip('v')
    upgrade_version = upgrade_version.lstrip('v')
    
    # Generate file path
    changes_file_path = get_changes_file_path(stack, current_version, upgrade_version)
    
    # Check if changes file already exists
    if changes_file_path.exists() and not force:
        print(f"Breaking changes file already exists at: {changes_file_path}")
        print("Use --force to regenerate the file.")
        return
    
    try:
        # Fetch changes from Perplexity API
        changes_content = fetch_changes_from_perplexity(stack, current_version, upgrade_version)
        
        # Add a header with metadata
        file_content = f"""# Breaking Changes: {stack} {current_version} → {upgrade_version}
> Generated on: {datetime.now().isoformat()}
> Stack: {stack}
> Current Version: {current_version}
> Upgrade Version: {upgrade_version}

{changes_content}"""
        
        # Write to file
        with open(changes_file_path, "w") as f:
            f.write(file_content)
        
        print(f"Breaking changes saved to: {changes_file_path}")
    except Exception as e:
        print(f"Error getting breaking changes: {str(e)}")
        sys.exit(1)


def get_report_file_path(directory: str, changes_file: str, output: Optional[str] = None) -> Path:
    """Generate the path for the report file."""
    if output:
        return Path(output)
    
    dir_name = os.path.basename(os.path.abspath(directory))
    changes_file_name = os.path.basename(changes_file)
    stack = changes_file_name.split('_')[0]
    
    stack_reports_dir = DATA_DIR / "reports" / stack
    stack_reports_dir.mkdir(exist_ok=True)
    
    report_name = f"{dir_name}_{changes_file_name.replace('_changes.md', '_gap.md')}"
    return stack_reports_dir / report_name


def find_files_by_stack(directory: str, stack: str) -> Tuple[List[str], int]:
    """Find all files for a specific technology stack in a directory."""
    try:
        # Get file extension pattern for the stack
        file_pattern = STACK_MAPPINGS.get(stack.lower(), {}).get("extensions", ["js"])
        
        # Get exclusion paths for the stack
        exclusions = STACK_MAPPINGS.get(stack.lower(), {}).get("exclude_paths", ["node_modules"])
        
        # Build the find command
        find_cmd = ["find", directory, "-type", "f"]
        
        # Add file extensions
        for extension in file_pattern:
            find_cmd.extend(["-name", f"*.{extension}"])
        
        # Add exclusion paths
        for exclusion in exclusions:
            find_cmd.extend(["-not", "-path", f"*{exclusion}*"])
        
        # Execute the find command
        result = subprocess.run(
            find_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        files = [line for line in result.stdout.splitlines() if line.strip()]
        
        return files, len(files)
        
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error finding files: {e.stderr}")


def concatenate_files(files: List[str]) -> Tuple[str, List[str]]:
    """Concatenate all files into a single string."""
    try:
        concatenated = ""
        file_list = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                rel_path = os.path.relpath(file_path)
                file_list.append(rel_path)
                concatenated += f"\n// FILE: {rel_path}\n{content}\n"
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {str(e)}")
        
        return concatenated, file_list
            
    except Exception as e:
        raise ValueError(f"Error concatenating files: {str(e)}")


def analyze_with_bedrock(concatenated_files: Tuple[str, List[str]], changes_content: str, directory: str) -> str:
    """Analyze code using AWS Bedrock."""
    print("Analyzing with AWS Bedrock...")
    
    aws_profile = os.environ.get('AWS_PROFILE', 'default')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    # Create prompt for Bedrock
    dir_name = os.path.basename(os.path.abspath(directory))
    content, file_list = concatenated_files
    
    # Extract version information from changes_content
    version_info = ""
    lines = changes_content.split('\n')
    for line in lines[:10]:  # Check first 10 lines for version info
        if "→" in line or "->" in line:
            version_info = line
            break
    
    prompt = f"""You are an expert developer tasked with analyzing code for compatibility issues when upgrading.

I will provide you with code files and a list of breaking changes for a SPECIFIC version upgrade. Your task is to:

1. IMPORTANT: Focus ONLY on the breaking changes for the specific version upgrade provided in the changes list. DO NOT analyze for any other version upgrades.
2. Identify compatibility issues in the code based ONLY on the breaking changes for this specific version upgrade.
3. Provide a detailed report of all issues found, including:
   - Files affected
   - Line numbers (if possible)
   - Explanation of the issue
   - Recommended solution
4. Analyze dependencies used in the directory that might be affected by this specific version upgrade
5. Provide a migration complexity assessment (Low, Medium, High) for this specific version upgrade only

The changes file you're analyzing is for: {version_info}
IMPORTANT: Your analysis should ONLY focus on compatibility issues for this specific version upgrade, not on any previous or future versions.

Here is the list of breaking changes to check against:

{changes_content}

Now, please analyze the following directory ({dir_name}) containing these files:
{chr(10).join(file_list)}

The concatenated content of all files is:

```
{content[:1000000] if len(content) > 1000000 else content}
```

Format your response as a Markdown document with the following sections:
1. Summary (focus only on this specific version upgrade)
2. Compatibility Issues (ONLY for this specific version upgrade, do not include issues from other versions)
3. Files Analysis (only files affected by this specific version upgrade)
4. Recommendations (specific to this version upgrade)
5. Migration Complexity (for this specific version upgrade only)
6. Dependencies Analysis (only dependencies affected by this specific version upgrade)

Be extremely detailed and thorough in your analysis, but ONLY for the specific version upgrade in the changes file. Do not analyze for any other version upgrades."""

    # Create temporary file for the input
    temp_input_path = BASE_DIR / "temp_bedrock_input.json"
    with open(temp_input_path, "w") as f:
        json.dump({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": prompt}]
        }, f)
    
    # Create temporary file for the output
    temp_output_path = BASE_DIR / "temp_bedrock_output.json"
    
    print("Sending request to AWS Bedrock...")
    
    # Call AWS Bedrock using the AWS CLI
    result = subprocess.run(
        [
            "aws", "bedrock-runtime", "invoke-model",
            "--model-id", "anthropic.claude-3-sonnet-20240229-v1:0",
            "--profile", aws_profile,
            "--region", aws_region,
            "--body", f"file://{temp_input_path}",
            "--cli-binary-format", "raw-in-base64-out",
            temp_output_path
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise ValueError(f"AWS CLI error: {result.stderr}")
    
    # Read the response
    with open(temp_output_path, "r") as f:
        response = json.load(f)
    
    # Clean up temporary files
    os.remove(temp_input_path)
    os.remove(temp_output_path)
    
    # Extract the content from the response
    if "content" in response and isinstance(response["content"], list):
        analysis_content = ""
        for block in response["content"]:
            if block.get("type") == "text":
                analysis_content += block["text"]
        
        print("Analysis with AWS Bedrock completed")
        return analysis_content
    else:
        raise ValueError("Unexpected response format from Bedrock")


@cli.command()
@click.option('--changes-file', required=True, help='Path to the changes file')
@click.option('--dir', required=True, help='Directory to analyze')
@click.option('--output', help='Output file path')
@click.option('--stack', default='node', help='Technology stack (e.g., node, java, python)')
def analyze_changes(changes_file: str, dir: str, output: Optional[str] = None, stack: str = 'node'):
    """Analyze codebase for compatibility issues."""
    # Check if changes file exists
    if not os.path.exists(changes_file):
        print(f"Changes file not found: {changes_file}")
        sys.exit(1)
    
    # Check if directory exists
    if not os.path.exists(dir) or not os.path.isdir(dir):
        print(f"Directory not found: {dir}")
        sys.exit(1)
    
    # Determine output file path
    output_path = get_report_file_path(dir, changes_file, output)
    
    try:
        # Read changes file
        with open(changes_file, 'r', encoding='utf-8') as f:
            changes_content = f.read()
        
        # Find and concatenate files based on stack
        files, file_count = find_files_by_stack(dir, stack)
        
        if not files:
            print(f"No {stack} files found in {dir}")
            sys.exit(1)
        
        concatenated_files = concatenate_files(files)
        
        # Analyze code
        analysis_content = analyze_with_bedrock(concatenated_files, changes_content, dir)
        
        # Write the output
        with open(output_path, 'w') as f:
            # Add metadata
            f.write(f"# Compatibility Analysis: {os.path.basename(dir)}\n")
            f.write(f"> Generated on: {datetime.now().isoformat()}\n")
            f.write(f"> Changes file: {os.path.basename(changes_file)}\n")
            f.write(f"> Stack: {stack}\n")
            f.write(f"> Analysis mode: AWS Bedrock\n")
            f.write(f"> Files analyzed: {file_count}\n\n")
            f.write(analysis_content)
        
        print(f"Analysis report saved to: {output_path}")
    except Exception as e:
        print(f"Error analyzing changes: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
