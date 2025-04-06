# Changelog

All notable changes to this project will be documented in this file.

## [0.1.4] - 2025-04-05

### Added
- Added natural language interface for generating code directly from prompts
- Added `generate` command for code generation from natural language
- Added direct mode interface without specifying a command (e.g., `bolor "create a function..."`)
- Added language auto-detection from natural language descriptions
- Implemented automatic code formatting and file saving capabilities

## [0.1.3] - 2025-04-05

### Fixed
- Fixed Phi-2 model loading issues with new fix_model_loading.py script
- Added fallback to smaller model when full model can't be downloaded
- Added model verification and automatic repair capabilities

## [0.1.2] - 2025-04-05

### Fixed
- Fixed dataset download errors by creating placeholder datasets
- Improved error handling in dataset loader and suppressed warning messages
- Fixed HuggingFace authentication errors by disabling datasets requiring auth
- Added `fix_dataset_errors.py` script to create placeholder datasets
- Added `setup-bolor.sh` for complete end-to-end setup

### Added
- Created comprehensive setup script that handles all installations
- Added placeholder datasets to allow offline usage

## [0.1.1] - 2025-04-05

### Fixed
- CLI script installation issue: Fixed issue where the `bolor` command wasn't in PATH
- Added helper scripts for CLI installation troubleshooting
- Included CLI wrapper script as an alternative method to run Bolor
- Fixed urllib3/requests dependency warnings by properly pinning dependency versions
- Added proper version constraints for all dependencies

### Added
- Added CHANGELOG.md file to track changes
- Added more detailed CLI installation instructions in documentation
- Added direct CLI installer via install-bolor-cli.sh

## [0.1.0] - 2025-04-05

### Added
- Initial release of Bolor
- Scan functionality for detecting code issues
- Fix functionality for automatically repairing detected issues
- Plan functionality for suggesting code improvements without modifying code
- deploy-check functionality for analyzing CI/CD configurations
- Support for Python, JavaScript/TypeScript, Java and C/C++ code analysis
- Local LLM integration with Phi-2
- Dataset integration with CodeXGLUE, MBPP, and QuixBugs
