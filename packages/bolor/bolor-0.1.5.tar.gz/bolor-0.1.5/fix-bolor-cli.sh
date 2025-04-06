#!/bin/bash
# This script fixes the Bolor command-line interface installation

# Find where the bolor script is located
BOLOR_SCRIPT=$(find ~/Library/Python -name bolor -type f 2>/dev/null)

if [ -z "$BOLOR_SCRIPT" ]; then
    echo "Could not find the bolor script. Make sure it's installed."
    exit 1
fi

echo "Found bolor script at: $BOLOR_SCRIPT"

# Option 1: Add Python bin directory to PATH
echo -e "\nOption 1: Add Python bin directory to PATH"
PYTHON_BIN_DIR=$(dirname "$BOLOR_SCRIPT")
echo "Would you like to add $PYTHON_BIN_DIR to your PATH? (y/n)"
read -r add_to_path

if [[ "$add_to_path" =~ ^[Yy]$ ]]; then
    echo 'export PATH="'$PYTHON_BIN_DIR':$PATH"' >> ~/.zshrc
    echo "Added to PATH in ~/.zshrc. Please restart your terminal or run 'source ~/.zshrc'"
fi

# Option 2: Create a symlink in /usr/local/bin
echo -e "\nOption 2: Create a symlink in /usr/local/bin"
echo "Would you like to create a symlink in /usr/local/bin? (y/n)"
read -r create_symlink

if [[ "$create_symlink" =~ ^[Yy]$ ]]; then
    if [ ! -d "/usr/local/bin" ]; then
        sudo mkdir -p /usr/local/bin
    fi
    sudo ln -sf "$BOLOR_SCRIPT" /usr/local/bin/bolor
    echo "Created symlink: /usr/local/bin/bolor -> $BOLOR_SCRIPT"
fi

# Option 3: Create an alias
echo -e "\nOption 3: Create a shell alias"
echo "Would you like to create an alias for bolor? (y/n)"
read -r create_alias

if [[ "$create_alias" =~ ^[Yy]$ ]]; then
    echo 'alias bolor="python3 -m bolor"' >> ~/.zshrc
    echo "Added alias to ~/.zshrc. Please restart your terminal or run 'source ~/.zshrc'"
fi

echo -e "\nDone! You should now be able to use the 'bolor' command."
echo "If you chose options that modify ~/.zshrc, run 'source ~/.zshrc' to apply changes to the current terminal session."
