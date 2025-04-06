# Bolor

![Version](https://img.shields.io/badge/version-0.1.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Bolor is a powerful CLI-based code repair tool that uses a locally embedded LLM (Phi-2) to automatically detect and fix bugs in your code. It leverages real bug-fix datasets for learning and retrieval, offering self-healing capabilities through advanced evolutionary algorithms.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [User Guide](#user-guide)
  - [Command Line Interface](#command-line-interface)
  - [Programmatic API](#programmatic-api)
  - [Configuration](#configuration)
  - [Advanced Usage](#advanced-usage)
  - [Working with Examples](#working-with-examples)
- [Supported Languages](#supported-languages)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Local LLM**: Uses a small embedded LLM (Phi-2) that runs entirely on your local machine
- **Bug Detection**: Scans your codebase to identify potential issues and bugs
- **Automatic Fixes**: Generates and applies fixes for detected issues
- **Evolutionary Approach**: Uses an evolutionary algorithm to generate and refine fix candidates
- **Real-world Bug Dataset**: Learns from popular bug-fix datasets (CodeXGLUE, MBPP, QuixBugs)
- **Planning Capabilities**: Suggests improvements to code without directly modifying it
- **Deployment Checks**: Analyzes CI/CD configurations to catch deployment issues

## Installation

### Using pip

You can install Bolor directly from PyPI:

```bash
pip install bolor
```

### From Source

To install from source:

```bash
git clone https://github.com/bolorproject/bolor.git
cd bolor
pip install -e .
```

### First Run

On first run, Bolor will automatically:
- Download the Phi-2 quantized model
- Download bug-fix datasets 
- Build a vector store for efficient retrieval

These resources are stored in `~/.bolor/` directory.

### Complete Installation with setup-bolor.sh

The fastest way to get started with Bolor is to use the comprehensive setup script:

```bash
# Download and run the setup script
curl -O https://raw.githubusercontent.com/bolorproject/bolor/main/setup-bolor.sh
curl -O https://raw.githubusercontent.com/bolorproject/bolor/main/fix_dataset_errors.py
curl -O https://raw.githubusercontent.com/bolorproject/bolor/main/fix_model_loading.py
chmod +x setup-bolor.sh fix_dataset_errors.py fix_model_loading.py
./setup-bolor.sh
```

This script will:
1. Fix dependency issues by installing compatible versions
2. Create placeholder datasets to avoid download errors
3. Fix model loading issues by verifying and downloading the Phi-2 model
4. Install the global CLI command

### CLI Installation Troubleshooting

If the `bolor` command is not found after installation, you can use one of these approaches:

1. **Run as a module** (works immediately, no setup needed):
   ```bash
   python3 -m bolor scan ./myproject
   ```

2. **Install the command globally** (recommended):
   ```bash
   # Download and run the installer script
   curl -O https://raw.githubusercontent.com/bolorproject/bolor/main/install-bolor-cli.sh
   chmod +x install-bolor-cli.sh
   ./install-bolor-cli.sh
   ```
   This creates a global command in `/usr/local/bin` that will work from any directory.

3. **Use the provided wrapper script**:
   ```bash
   # Download the wrapper script
   curl -O https://raw.githubusercontent.com/bolorproject/bolor/main/bolor-cli
   chmod +x bolor-cli
   
   # Use the wrapper
   ./bolor-cli scan ./myproject
   ```

### Model Loading Issues

If you see errors like `Failed to create LLM 'phi' from '/Users/username/.bolor/models/phi-2/phi-2.Q4_K_M.gguf'`, use the model fixer script:

```bash
# Download and run the model fixer
curl -O https://raw.githubusercontent.com/bolorproject/bolor/main/fix_model_loading.py
chmod +x fix_model_loading.py
./fix_model_loading.py
```

This script will:
1. Verify if the model file exists and is valid
2. Download the Phi-2 model if needed
3. Fall back to a smaller model if the main one can't be downloaded
4. Test if the model can be loaded correctly
5. Update the configuration to use the available model

## User Guide

### Command Line Interface

Bolor provides a comprehensive command-line interface with several commands and options.

#### Global Options

Options that apply to all commands:

```
--verbose, -v         Enable verbose output
--help                Show help message
```

#### Scanning for Issues

```bash
bolor scan [OPTIONS] [PROJECT_PATH]
```

Arguments:
- `PROJECT_PATH`: Path to the project to scan (default: current directory)

Options:
- `--fix, -f`: Automatically apply fixes for detected issues
- `--verbose, -v`: Enable verbose output

Examples:

```bash
# Scan the current directory
bolor scan

# Scan a specific project
bolor scan ./my_project

# Scan and fix issues
bolor scan ./my_project --fix

# Scan with verbose output
bolor scan ./my_project --verbose
```

#### Planning Improvements

```bash
bolor plan [OPTIONS] [PROJECT_PATH]
```

Arguments:
- `PROJECT_PATH`: Path to the project to analyze (default: current directory)

Options:
- `--format, -f`: Output format (text, markdown, json) (default: text)
- `--verbose, -v`: Enable verbose output

Examples:

```bash
# Get improvement suggestions for current directory
bolor plan

# Get suggestions for a specific project
bolor plan ./my_project

# Get suggestions in markdown format
bolor plan ./my_project --format markdown

# Get suggestions in JSON format
bolor plan ./my_project --format json
```

#### Checking Deployment Configurations

```bash
bolor deploy-check [OPTIONS] [PROJECT_PATH]
```

Arguments:
- `PROJECT_PATH`: Path to the project to check (default: current directory)

Options:
- `--verbose, -v`: Enable verbose output

Examples:

```bash
# Check deployment configurations for current directory
bolor deploy-check

# Check a specific project
bolor deploy-check ./my_project
```

#### Generating Code from Natural Language

```bash
bolor generate [OPTIONS] PROMPT
```

Arguments:
- `PROMPT`: Natural language description of what to generate

Options:
- `--output, -o`: File to save the generated code to
- `--language, -l`: Programming language to generate in (auto-detected if not specified)
- `--no-comments`: Generate code without explanatory comments
- `--verbose, -v`: Enable verbose output

Examples:

```bash
# Generate Python code for a function
bolor generate "create a function to download a file from a URL"

# Generate a GitHub Actions workflow and save it to a file
bolor generate "create GitHub action for Python testing" --output .github/workflows/test.yml

# Generate a React component without comments
bolor generate "create a React component for a user profile" --language javascript --no-comments
```

#### Natural Language Interface (Direct Mode)

Bolor also supports a direct natural language interface without specifying a command:

```bash
bolor "PROMPT"
```

This is equivalent to `bolor generate "PROMPT"` and provides a quick way to generate code from natural language descriptions.

Examples:

```bash
# Generate a Python function to calculate Fibonacci numbers
bolor "create a function to calculate Fibonacci numbers"

# Generate a GitHub Actions workflow for AWS deployment
bolor "create GitHub action for AWS deployment"
```

#### Downloading Resources

```bash
bolor download-resources [OPTIONS]
```

Options:
- `--force, -f`: Force re-download of resources even if they exist
- `--verbose, -v`: Enable verbose output

Examples:

```bash
# Download required resources
bolor download-resources

# Force re-download of resources
bolor download-resources --force
```

### Programmatic API

Bolor can also be used programmatically in your Python code.

#### Basic Usage

```python
from pathlib import Path
from bolor.utils.config import Config
from bolor.agent.scanner import Scanner
from bolor.agent.fixer import Fixer

# Create configuration
config = Config()

# Create scanner
scanner = Scanner(config)

# Scan a file or directory
file_path = Path("./my_project/file.py")
issues = scanner.scan_file(file_path)

# Or scan an entire directory
# issues = scanner.scan_directory(Path("./my_project"))

# Print detected issues
for issue in issues:
    print(f"Issue: {issue.issue_type.value} - {issue.description}")
    print(f"  Line: {issue.line_number}")

# Fix the issues
fixer = Fixer(config)
fixed_issues = fixer.fix_issues(issues)

# Print fixed issues
for issue in fixed_issues:
    print(f"Fixed: {issue.issue_type.value} - {issue.description}")
```

#### Getting Improvement Suggestions

```python
from pathlib import Path
from bolor.utils.config import Config
from bolor.agent.planner import Planner

# Create configuration
config = Config()
config.set("output_format", "markdown")  # Optional: set output format

# Create planner
planner = Planner(config)

# Generate improvement suggestions
project_path = Path("./my_project")
suggestions = planner.analyze_project(project_path)

# Print suggestions
for suggestion in suggestions:
    print(f"Suggestion: {suggestion.title}")
    print(f"  {suggestion.description}")
    if suggestion.code_example:
        print(f"  Example:\n{suggestion.code_example}")
```

#### Checking Deployment Configurations

```python
from pathlib import Path
from bolor.utils.config import Config
from bolor.agent.scanner import Scanner

# Create configuration
config = Config()

# Create scanner
scanner = Scanner(config)

# Check deployment configurations
project_path = Path("./my_project")
issues = scanner.scan_ci_config(project_path)

# Print deployment issues
for issue in issues:
    print(f"Deployment issue: {issue.description}")
    if issue.details:
        print(f"  Details: {issue.details}")
    if issue.suggestions:
        print("  Suggestions:")
        for suggestion in issue.suggestions:
            print(f"    - {suggestion}")
```

### Configuration

Bolor can be configured through a configuration object. The configuration affects all aspects of Bolor's behavior.

#### Default Configuration

The default configuration is appropriate for most use cases and includes:

- Model settings (Phi-2 with appropriate parameters)
- Dataset settings (which datasets to use)
- Evolution settings (population size, mutation rate, etc.)
- Scanner settings (file types to scan, directories to exclude)
- Path settings (where to store models, datasets, etc.)

#### Custom Configuration

You can customize the configuration either programmatically or through a JSON file.

Programmatically:

```python
from bolor.utils.config import Config

config = Config()

# Change model settings
config.set("model.temperature", 0.5)  # Control randomness of the LLM

# Change evolution settings
config.set("evolution.population_size", 30)  # Larger population
config.set("evolution.generations", 15)  # More generations
config.set("evolution.mutation_rate", 0.3)  # Higher mutation rate

# Change scanner settings
config.set("scanner.file_extensions", [".py", ".js"])  # Only scan Python and JavaScript files
config.set("scanner.exclude_patterns", ["node_modules", "venv", "test"])  # Exclude these directories
```

From a JSON file:

```python
from bolor.utils.config import Config

config = Config("path/to/config.json")
```

Where `config.json` might look like:

```json
{
  "model": {
    "temperature": 0.5,
    "max_length": 1024
  },
  "evolution": {
    "population_size": 30,
    "generations": 15,
    "mutation_rate": 0.3
  },
  "scanner": {
    "file_extensions": [".py", ".js"],
    "exclude_patterns": ["node_modules", "venv", "test"]
  }
}
```

### Advanced Usage

#### Working with Specific File Types

Bolor supports multiple languages, but you can focus on specific file types:

```python
from bolor.utils.config import Config
from bolor.agent.scanner import Scanner

config = Config()
config.set("scanner.file_extensions", [".py"])  # Only scan Python files

scanner = Scanner(config)
issues = scanner.scan_directory(Path("./my_project"))
```

#### Custom Fix Evaluation

You can customize how fix candidates are evaluated:

```python
from bolor.utils.config import Config
from bolor.agent.fixer import Fixer
from bolor.agent.models import Issue

# Custom evaluation function
def custom_evaluator(candidate, issue, file_content):
    # Your custom evaluation logic here
    # Return a fitness score between 0.0 and 1.0
    return 0.8

# Create configuration
config = Config()

# Create fixer with custom evaluator
fixer = Fixer(config)
fixer._evaluate_candidate = custom_evaluator

# Use the fixer normally
issues = [...]  # Your issues
fixed_issues = fixer.fix_issues(issues)
```

#### Debugging Fixes

For debugging fix generation, you can enable verbose logging:

```python
import logging
from bolor.utils.config import Config
from bolor.agent.fixer import Fixer

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create configuration with verbose output
config = Config()
config.set("verbose", True)

# Create fixer
fixer = Fixer(config)
```

### Working with Examples

Bolor comes with examples to help you understand how it works.

#### Running the Examples

```bash
# Clone the repository
git clone https://github.com/bolorproject/bolor.git
cd bolor

# Install Bolor in development mode
pip install -e .

# Run the example script
python examples/use_bolor.py
```

This will demonstrate:
1. Scanning the example buggy code
2. Generating fixes for the detected issues
3. Suggesting improvements

#### Creating Your Own Examples

You can create your own example files with issues to see how Bolor handles them:

1. Create a file with intentional issues (syntax errors, logical errors, etc.)
2. Run Bolor on the file to see the detected issues
3. Use the `--fix` option to see how Bolor fixes the issues

## Supported Languages

Bolor currently provides scanning and fixing capabilities for:

- **Python**: Full support for syntax errors, logical errors, and code quality issues
- **JavaScript/TypeScript**: Support for common issues
- **Java**: Basic support for syntax and common issues
- **C/C++**: Basic support for common issues

The level of support varies by language, with Python having the most comprehensive support due to its use of Python's AST for analysis.

## Architecture

Bolor is built with a modular architecture inspired by evolutionary systems:

```
bolor/
├── agent/            # Core agents for scanning, fixing, and planning
│   ├── scanner.py    # Code scanning and issue detection
│   ├── fixer.py      # Code fixing with evolutionary approach
│   ├── planner.py    # Improvement suggestions
│   └── llm_wrapper.py # LLM integration
├── evolution/        # Evolutionary algorithm components
│   ├── candidate.py  # Fix candidates
│   └── fitness.py    # Fitness evaluation
├── utils/            # Utilities and helpers
└── models/           # Embedded Phi-2 model
```

The fix generation process follows an evolutionary approach:
1. Generate initial fix candidates using LLM and similar bug patterns
2. Evaluate candidates based on syntax correctness and other metrics
3. Select the best candidates and create new ones through mutation and crossover
4. Repeat until a satisfactory fix is found or generation limit is reached

## Troubleshooting

### Common Issues

#### Model Download Issues

**Problem**: Failed to download the Phi-2 model.

**Solution**: 
- Check your internet connection
- Manually download the model from `https://huggingface.co/TheBloke/phi-2-GGUF`
- Place it in `~/.bolor/models/phi-2/`

#### Memory Issues

**Problem**: Running out of memory when using Bolor.

**Solution**:
- Use a smaller variant of the model by setting `config.set("model.file", "phi-2.Q2_K.gguf")`
- Limit the files being scanned by using more specific paths
- Increase your system's swap space

#### ModuleNotFoundError

**Problem**: Getting `ModuleNotFoundError` when importing Bolor.

**Solution**:
- Ensure Bolor is installed (`pip install bolor`)
- If using from source, ensure you're in the correct directory or install with `pip install -e .`

#### Unexpected Fixes

**Problem**: Bolor is generating fixes that don't seem correct.

**Solution**:
- Try with `--verbose` to see more details about the fix generation process
- Adjust the configuration to control the fix generation:
  - Decrease `model.temperature` for more deterministic fixes
  - Increase `evolution.generations` for more refinement

### Getting Help

If you encounter issues not covered here:
- Check the documentation in the examples directory
- Submit an issue on the GitHub repository
- Contact the maintainers at support@bolorproject.com

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Bug Reports and Feature Requests**: Use the GitHub issue tracker
2. **Code Contributions**:
   - Fork the repository
   - Create a new branch for your feature or bugfix
   - Add tests for your changes
   - Run the test suite to ensure everything works
   - Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/bolorproject/bolor.git
cd bolor

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

Bolor is released under the MIT License. See the LICENSE file for details.
