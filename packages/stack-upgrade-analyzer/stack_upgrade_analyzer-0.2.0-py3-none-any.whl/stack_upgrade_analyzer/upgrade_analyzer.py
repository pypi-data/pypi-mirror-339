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
import re

# Import utility functions
from .utils import get_package_root, get_data_dir, get_changes_dir

# Import required packages
import requests
from dotenv import load_dotenv
import inquirer

# Set up paths
BASE_DIR = get_package_root()
DATA_DIR = get_data_dir()
CHANGES_DIR = get_changes_dir()
REPORTS_DIR = DATA_DIR / "reports"

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
REPORTS_DIR.mkdir(exist_ok=True)

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
    
    stack_reports_dir = REPORTS_DIR / stack
    stack_reports_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    # Extract file content and file paths
    concatenated_content, file_paths = concatenated_files
    
    # Construct the prompt
    prompt = f"""
You are an expert software developer analyzing code compatibility issues when upgrading technology stacks.

I have a codebase I want to upgrade, and I need to identify potential compatibility issues.

Here are the breaking changes between versions:
```
{changes_content}
```

Here is the code I want to analyze:
```
{concatenated_content}
```

Please analyze the code and identify any compatibility issues when upgrading. For each issue:
1. Specify the file path and line number where the issue occurs
2. Explain why it's an issue
3. Suggest how to fix it
4. Rate the severity (Critical, High, Medium, Low)

Format your response as a Markdown document with sections for each type of issue.
If there are no issues, state that the code is compatible with the upgrade.
"""
    
    # Set up AWS Bedrock client
    try:
        print("Sending request to AWS Bedrock...")
        
        # Use AWS CLI to invoke Bedrock
        aws_cmd = [
            "aws", "bedrock-runtime", "invoke-model",
            "--model-id", "anthropic.claude-3-sonnet-20240229-v1:0",
            "--profile", "tpm-pprod",
            "--body", json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }),
            "--cli-binary-format", "raw-in-base64-out",
            "output.json"
        ]
        
        # Run the AWS CLI command
        result = subprocess.run(aws_cmd, capture_output=True, text=True, check=True)
        
        # Read the output file
        with open("output.json", "r") as f:
            response = json.load(f)
        
        # Clean up the output file
        if os.path.exists("output.json"):
            os.remove("output.json")
        
        # Extract the response content
        if "content" in response and len(response["content"]) > 0:
            for content_item in response["content"]:
                if content_item["type"] == "text":
                    return content_item["text"]
        
        raise ValueError("Unexpected response format from Bedrock")
    except subprocess.CalledProcessError as e:
        print(f"AWS CLI error: \n{e.stderr}")
        if "AccessDeniedException" in e.stderr:
            return """
# Analysis Error: AWS Bedrock Access Denied

## Error Details
The analysis could not be completed because the AWS Bedrock service returned an access denied error.

### Possible Reasons:
1. The AWS profile 'tpm-pprod' may not have the necessary permissions to access the Bedrock service
2. The Anthropic Claude 3 Sonnet model may not be enabled for your AWS account
3. There might be an issue with your AWS credentials

### Recommended Actions:
1. Verify that your AWS profile has the correct permissions
2. Ensure that the Anthropic Claude 3 Sonnet model is enabled in your AWS Bedrock console
3. Check your AWS credentials and try again
4. Contact your AWS administrator for assistance

You can still manually review your code against the breaking changes document to identify potential issues.
"""
        else:
            return f"""
# Analysis Error: AWS Bedrock Service Error

## Error Details
The analysis could not be completed due to an error with the AWS Bedrock service.

### Error Message:
```
{e.stderr}
```

### Recommended Actions:
1. Check your AWS credentials and permissions
2. Ensure you have access to the AWS Bedrock service
3. Try again later or contact your AWS administrator for assistance

You can still manually review your code against the breaking changes document to identify potential issues.
"""
    except Exception as e:
        print(f"Error analyzing with Bedrock: {str(e)}")
        return f"""
# Analysis Error: Unexpected Error

## Error Details
The analysis could not be completed due to an unexpected error.

### Error Message:
```
{str(e)}
```

### Recommended Actions:
1. Check your input files and try again
2. Ensure you have the necessary permissions and credentials
3. Contact support if the issue persists

You can still manually review your code against the breaking changes document to identify potential issues.
"""


def analyze_changes(changes_file: str, dir: str, output: Optional[str] = None, stack: str = 'node'):
    """Analyze codebase for compatibility issues."""
    # Check if changes file exists
    if not os.path.exists(changes_file):
        raise FileNotFoundError(f"Changes file not found: {changes_file}")
    
    # Check if directory exists
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Directory not found: {dir}")
    
    # Read changes file
    with open(changes_file, 'r') as f:
        changes_content = f.read()
    
    # Get version information from the changes file
    versions_match = re.search(r'# Breaking Changes: \w+ (\d+(?:\.\d+)*) → (\d+(?:\.\d+)*)', changes_content)
    if not versions_match:
        raise ValueError("Could not determine versions from changes file")
    
    current_version = versions_match.group(1)
    upgrade_version = versions_match.group(2)
    
    # Create reports directory if it doesn't exist
    reports_dir = REPORTS_DIR / stack
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Set default output path if not provided
    if not output:
        output = reports_dir / f"{current_version}_to_{upgrade_version}_report.md"
    
    # Collect all files in the directory
    files = []
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(('.js', '.jsx', '.ts', '.tsx')):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                files.append((file_path, content))
    
    # Analyze code
    analysis_content = analyze_with_bedrock(concatenate_files([file[0] for file in files]), changes_content, dir)
    
    # Write the output
    with open(output, 'w') as f:
        # Add metadata
        f.write(f"# Compatibility Analysis: {os.path.basename(dir)}\n")
        f.write(f"> Generated on: {datetime.now().isoformat()}\n")
        f.write(f"> Changes file: {os.path.basename(changes_file)}\n")
        f.write(f"> Stack: {stack}\n")
        f.write(f"> Analysis mode: AWS Bedrock\n")
        f.write(f"> Files analyzed: {len(files)}\n\n")
        f.write(analysis_content)
    
    print(f"Analysis report saved to: {output}")


if __name__ == "__main__":
    pass
