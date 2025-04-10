# Stack Upgrade Analyzer

A tool for analyzing code compatibility issues when upgrading technology stacks.

[![PyPI version](https://img.shields.io/pypi/v/stack-upgrade-analyzer.svg)](https://pypi.org/project/stack-upgrade-analyzer/)
[![Python Versions](https://img.shields.io/pypi/pyversions/stack-upgrade-analyzer.svg)](https://pypi.org/project/stack-upgrade-analyzer/)
[![License](https://img.shields.io/pypi/l/stack-upgrade-analyzer.svg)](https://github.com/trilogy-group/upgrade-analyzer/blob/main/LICENSE)

## Features

- **Multi-Stack Support**: Analyze code compatibility for various technology stacks (Node.js, Java, Python, etc.)
- **Breaking Changes Documentation**: Fetch comprehensive breaking changes documentation between versions
- **Codebase Analysis**: Analyze your codebase for compatibility issues using AWS Bedrock
- **Detailed Reports**: Generate detailed reports of compatibility issues with recommendations

## Installation

```bash
pip install stack-upgrade-analyzer
```

## Requirements

- Python 3.7+
- AWS CLI configured with access to Bedrock
- Perplexity API key (for fetching breaking changes documentation)

## Configuration

Before using the tool, configure your API keys:

```bash
stack-upgrade-analyzer config
```

This will prompt you to enter your Perplexity API key and AWS configuration.

## Usage

### Fetch Breaking Changes

```bash
# Fetch breaking changes between Node.js versions
stack-upgrade-analyzer get-changes-cmd --stack node --current-version 14.0 --upgrade-version 16.0

# Fetch breaking changes between Java versions
stack-upgrade-analyzer get-changes-cmd --stack java --current-version 11 --upgrade-version 17
```

### Analyze Codebase

```bash
# Analyze a Node.js codebase
stack-upgrade-analyzer analyze-changes-cmd --changes-file changes/node/14.0_16.0_changes.md --dir /path/to/your/project --stack node

# Analyze a Java codebase
stack-upgrade-analyzer analyze-changes-cmd --changes-file changes/java/11_17_changes.md --dir /path/to/your/project --stack java
```

## Supported Stacks

- Node.js
- Java
- Python
- Ruby
- C#
- PHP

## How It Works

1. **Fetch Breaking Changes**: The tool uses the Perplexity API to fetch comprehensive breaking changes documentation between versions.
2. **Analyze Codebase**: The tool analyzes your codebase for compatibility issues using AWS Bedrock.
3. **Generate Report**: The tool generates a detailed report of compatibility issues with recommendations.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
