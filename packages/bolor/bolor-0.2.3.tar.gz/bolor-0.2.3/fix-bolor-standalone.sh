#!/bin/bash
# Standalone Bolor model fixer
# This script directly fixes model loading issues without relying on Bolor's update command

echo "============================================================"
echo " Bolor Model Fixer - Direct Solution"
echo "============================================================"

# Determine Bolor's data directory
BOLOR_DIR="$HOME/.bolor"
MODEL_NAME="phi-2"
MODEL_DIR="$BOLOR_DIR/models/$MODEL_NAME"
CONFIG_DIR="$BOLOR_DIR/config"
CONFIG_FILE="$CONFIG_DIR/config.json"

# Create directories
echo "Creating model directories..."
mkdir -p "$MODEL_DIR"
mkdir -p "$CONFIG_DIR"

# Use curl instead of relying on bolor's update command
FALLBACK_FILE="phi-2.Q2_K.gguf"
FALLBACK_URL="https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q2_K.gguf"
FALLBACK_PATH="$MODEL_DIR/$FALLBACK_FILE"

# Download model if it doesn't exist
if [ ! -f "$FALLBACK_PATH" ]; then
  echo "Downloading model from $FALLBACK_URL"
  echo "This may take a while (~1.5GB)..."
  curl -L "$FALLBACK_URL" --output "$FALLBACK_PATH" --progress-bar
  
  if [ $? -ne 0 ]; then
    echo "Failed to download model. Please check your internet connection and try again."
    exit 1
  fi
  
  echo "Download completed: $FALLBACK_PATH"
else
  echo "Model file already exists at $FALLBACK_PATH"
fi

# Create simple config file that should work in all cases
echo '{
  "model": {
    "name": "phi-2",
    "file": "phi-2.Q2_K.gguf",
    "type": "llama"
  }
}' > "$CONFIG_FILE"

echo "Created configuration file at $CONFIG_FILE"
echo ""
echo "Model files and configuration have been fixed."
echo "You can now use Bolor with the following commands:"
echo "  bolor scan [directory]"
echo "  bolor plan [directory]"
echo "  bolor generate \"your prompt\""
echo ""
echo "If you still encounter issues, try reinstalling ctransformers:"
echo "  pip install --force-reinstall ctransformers==0.2.24"
