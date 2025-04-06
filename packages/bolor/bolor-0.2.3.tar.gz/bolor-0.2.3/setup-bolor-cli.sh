#!/bin/bash
# Consolidated setup script for Bolor CLI
# This script combines the functionality of install-bolor-cli.sh and fix-bolor-cli.sh

# Make script executable
if [ ! -x "$0" ]; then
    chmod +x "$0"
    echo "Made script executable"
fi

echo "==== Bolor CLI Setup ===="
echo "This script will set up the Bolor command-line interface for direct use."

# Determine if we're in the Bolor directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BOLOR_CLI="$DIR/bolor-cli"

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

# Setup options
echo -e "\n==== Installation Options ===="
echo "Choose how you want to set up the 'bolor' command:"
echo "1) Create a system-wide command in /usr/local/bin (recommended, requires sudo)"
echo "2) Add alias to your shell profile (works only in interactive shells)"
echo "3) Add script directory to your PATH (makes all scripts in this dir available)"
echo "4) Create a symlink in your home bin directory (~/bin)"
echo "5) Exit without changes"
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
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
        ;;
        
    2)
        # Add alias to shell profile
        SHELL_PROFILE=""
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_PROFILE="$HOME/.zshrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            SHELL_PROFILE="$HOME/.bash_profile"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_PROFILE="$HOME/.bashrc"
        else
            echo "Could not find shell profile (.zshrc, .bash_profile, or .bashrc)."
            echo "Creating .zshrc file..."
            SHELL_PROFILE="$HOME/.zshrc"
            touch "$SHELL_PROFILE"
        fi
        
        echo "Adding alias to $SHELL_PROFILE..."
        
        # Check if alias already exists
        if grep -q "alias bolor=" "$SHELL_PROFILE"; then
            echo "Alias for bolor already exists in $SHELL_PROFILE. Updating it..."
            sed -i.bak '/alias bolor=/d' "$SHELL_PROFILE"
        fi
        
        # Add the alias
        echo -e '\n# Bolor CLI alias' >> "$SHELL_PROFILE"
        echo "alias bolor='$BOLOR_CLI'" >> "$SHELL_PROFILE"
        
        echo "✅ Alias added to $SHELL_PROFILE"
        echo "To use it in this terminal, run: source $SHELL_PROFILE"
        echo "After that, you can run 'bolor' from any directory."
        ;;
        
    3)
        # Add script directory to PATH
        SHELL_PROFILE=""
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_PROFILE="$HOME/.zshrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            SHELL_PROFILE="$HOME/.bash_profile"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_PROFILE="$HOME/.bashrc"
        else
            echo "Could not find shell profile (.zshrc, .bash_profile, or .bashrc)."
            echo "Creating .zshrc file..."
            SHELL_PROFILE="$HOME/.zshrc"
            touch "$SHELL_PROFILE"
        fi
        
        echo "Adding script directory to PATH in $SHELL_PROFILE..."
        
        # Check if PATH already includes this directory
        if grep -q "export PATH=\"$DIR:" "$SHELL_PROFILE"; then
            echo "PATH already includes $DIR in $SHELL_PROFILE"
        else
            echo -e '\n# Add Bolor CLI directory to PATH' >> "$SHELL_PROFILE"
            echo "export PATH=\"$DIR:\$PATH\"" >> "$SHELL_PROFILE"
            echo "✅ Added to PATH in $SHELL_PROFILE"
        fi
        
        echo "To update PATH in this terminal, run: source $SHELL_PROFILE"
        echo "After that, you can run './bolor-cli' or create a symlink named 'bolor' to use it directly."
        ;;
        
    4)
        # Create symlink in ~/bin
        HOME_BIN="$HOME/bin"
        
        # Create ~/bin if it doesn't exist
        if [ ! -d "$HOME_BIN" ]; then
            echo "Creating $HOME_BIN directory..."
            mkdir -p "$HOME_BIN"
        fi
        
        # Check if ~/bin is in PATH
        if [[ ":$PATH:" != *":$HOME_BIN:"* ]]; then
            SHELL_PROFILE=""
            if [ -f "$HOME/.zshrc" ]; then
                SHELL_PROFILE="$HOME/.zshrc"
            elif [ -f "$HOME/.bash_profile" ]; then
                SHELL_PROFILE="$HOME/.bash_profile"
            elif [ -f "$HOME/.bashrc" ]; then
                SHELL_PROFILE="$HOME/.bashrc"
            else
                echo "Could not find shell profile. Creating .zshrc..."
                SHELL_PROFILE="$HOME/.zshrc"
                touch "$SHELL_PROFILE"
            fi
            
            echo "Adding ~/bin to PATH in $SHELL_PROFILE..."
            echo -e '\n# Add ~/bin to PATH' >> "$SHELL_PROFILE"
            echo "export PATH=\"$HOME_BIN:\$PATH\"" >> "$SHELL_PROFILE"
            echo "Added ~/bin to PATH in $SHELL_PROFILE"
        fi
        
        # Create the symlink
        SYMLINK_PATH="$HOME_BIN/bolor"
        echo "Creating symlink: $SYMLINK_PATH -> $BOLOR_CLI"
        ln -sf "$BOLOR_CLI" "$SYMLINK_PATH"
        
        echo "✅ Symlink created in ~/bin"
        if [[ ":$PATH:" != *":$HOME_BIN:"* ]]; then
            echo "To update PATH in this terminal, run: source $SHELL_PROFILE"
        fi
        echo "After that, you can run 'bolor' from any directory."
        ;;
        
    5)
        echo "Exiting without changes."
        exit 0
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo -e "\nSetup complete! 🎉"
echo "If you encounter any issues, consider reinstalling Bolor with 'pip install -e .' from the project directory."
