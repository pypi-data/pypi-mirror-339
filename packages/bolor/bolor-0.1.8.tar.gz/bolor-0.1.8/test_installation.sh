#!/bin/bash
# Script to test Bolor installation

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Bolor Installation Test${NC}"
echo "======================================"

# Check if Bolor is installed via pip
echo -e "\n${YELLOW}1. Checking pip installation:${NC}"
if pip show bolor > /dev/null 2>&1; then
    VERSION=$(pip show bolor | grep Version | awk '{print $2}')
    echo -e "${GREEN}✓ Bolor is installed (Version: $VERSION)${NC}"
else
    echo -e "${RED}✗ Bolor is not installed via pip${NC}"
    echo "Try running: pip install bolor"
    exit 1
fi

# Check if the module can be imported
echo -e "\n${YELLOW}2. Testing Python import:${NC}"
if python3 -c "import bolor" 2>/dev/null; then
    echo -e "${GREEN}✓ Bolor can be imported in Python${NC}"
else
    echo -e "${RED}✗ Bolor cannot be imported in Python${NC}"
    echo "This might indicate a problem with the installation. Try reinstalling."
    exit 1
fi

# Test running as a module
echo -e "\n${YELLOW}3. Testing module execution:${NC}"
if python3 -m bolor --help > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Bolor can be run as a module${NC}"
else
    echo -e "${RED}✗ Bolor cannot be run as a module${NC}"
    echo "This might indicate a problem with the package structure."
    exit 1
fi

# Test direct command
echo -e "\n${YELLOW}4. Testing direct command execution:${NC}"
if which bolor > /dev/null 2>&1; then
    BOLOR_PATH=$(which bolor)
    echo -e "${GREEN}✓ Bolor command is available at: $BOLOR_PATH${NC}"
    
    if bolor --help > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Bolor command executes successfully${NC}"
    else
        echo -e "${RED}✗ Bolor command exists but doesn't execute correctly${NC}"
        echo "This might indicate a problem with the script permissions or entry point."
    fi
else
    echo -e "${YELLOW}⚠ Bolor command is not in PATH${NC}"
    echo "This is likely due to the Python bin directory not being in your PATH."
    echo "You have several options:"
    echo "  1. Run using: python3 -m bolor"
    echo "  2. Use the bolor-cli wrapper script: ./bolor-cli"
    echo "  3. Use the fix-bolor-cli.sh script to fix the PATH issue: ./fix-bolor-cli.sh"
fi

echo -e "\n${YELLOW}5. Testing available commands:${NC}"
echo "Attempting to list available commands..."
python3 -m bolor --help

echo -e "\n${GREEN}Installation test complete!${NC}"
