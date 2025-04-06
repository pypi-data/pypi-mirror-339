#!/bin/bash
# Automatic deployment script for Bolor CLI
# This runs setup-bolor-cli.sh in non-interactive mode, selecting option 1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BOLOR_CLI="$DIR/bolor-cli"

echo "==== Automatic Bolor CLI Deployment ===="
echo "This script will install the Bolor CLI globally."

if [ ! -f "$BOLOR_CLI" ]; then
    echo "Error: bolor-cli script not found in current directory."
    echo "Please run this script from the Bolor project directory."
    exit 1
fi

echo "Found bolor-cli script at: $BOLOR_CLI"
echo "Making bolor-cli executable..."
chmod +x "$BOLOR_CLI"

# Check if Python is installed and get its path
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Find the bolor module, trying multiple methods
# Method 1: Try to find an existing installation
BOLOR_PATH=""
EXISTING_BOLOR=$(find ~/Library/Python -name bolor -type f 2>/dev/null | head -n 1)
if [ -n "$EXISTING_BOLOR" ]; then
    BOLOR_PATH=$(dirname "$EXISTING_BOLOR")
    echo "Found existing Bolor installation at: $EXISTING_BOLOR"
fi

# Method 2: Check if we're in a Python path
PYTHON_PATHS=$(python3 -c "import sys; print('\n'.join(sys.path))" | grep -v "__pycache__" | grep -v ".pyc")
for path in $PYTHON_PATHS; do
    if [ -d "$path/bolor" ]; then
        BOLOR_PATH="$path/bolor"
        echo "Found Bolor module in Python path: $BOLOR_PATH"
        break
    fi
done

# Method 3: Use the current directory if it contains bolor module
if [ -z "$BOLOR_PATH" ] && [ -d "$DIR/bolor" ]; then
    BOLOR_PATH="$DIR/bolor"
    echo "Using local Bolor module in current directory"
fi

if [ -z "$BOLOR_PATH" ]; then
    echo "Warning: Could not locate the Bolor module. The script may not work correctly."
    echo "You might need to install Bolor with 'pip install -e .' first."
fi

# Run the requests patcher to silence warnings if it exists
if [ -f "$DIR/patch_requests.py" ]; then
    echo "Patching requests library to silence warnings..."
    python3 "$DIR/patch_requests.py"
fi

# Create system-wide command
GLOBAL_PATH="/usr/local/bin/bolor"
echo "Creating system-wide command at $GLOBAL_PATH..."

# Create the script content
cat > /tmp/bolor_wrapper << 'EOF'
#!/bin/bash
# Global wrapper for Bolor CLI

# Handle special case for generate command
if [[ "$1" == "generate" && $# -ge 2 ]]; then
    # Extract the prompt and other arguments
    PROMPT="$2"
    shift 2  # Remove 'generate' and the prompt
    
    # Run the command with properly positioned arguments
    PYTHONWARNINGS=ignore python3 -c "import sys; from bolor.__main__ import main; sys.argv[0] = 'bolor'; sys.exit(main())" "generate" "$PROMPT" "$@"
else
    # Run normally for other commands
    PYTHONWARNINGS=ignore python3 -c "import sys; from bolor.__main__ import main; sys.argv[0] = 'bolor'; sys.exit(main())" "$@"
fi
EOF

# Install it with sudo
sudo mv /tmp/bolor_wrapper "$GLOBAL_PATH"
sudo chmod +x "$GLOBAL_PATH"

echo "✅ Installation complete! You can now run 'bolor' from any directory."
echo "Try it now with: bolor --help"

echo -e "\nDeployment complete! 🎉"
echo "The 'bolor' command is now available system-wide."
echo "You can use it directly with commands like: bolor generate \"login HTML\" --output login.html"
