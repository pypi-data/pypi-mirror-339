#!/bin/bash
# Build and upload Bolor to PyPI

echo "Building and uploading Bolor v$(grep -oP "version=\"\K[^\"]*" setup.py) to PyPI"

# Clean up previous build artifacts
echo "Cleaning up previous build artifacts..."
rm -rf dist/ build/ *.egg-info/

# Install required packages if not already installed
echo "Making sure build tools are installed..."
pip install --upgrade pip wheel build twine

# Build the package
echo "Building the package..."
python3 -m build

# Check the package
echo "Checking the package..."
python3 -m twine check dist/*

echo "Ready to upload to PyPI!"
echo "-------------------------"
echo "Options:"
echo "1. Upload to Test PyPI (for testing)"
echo "2. Upload to real PyPI (for production)"
echo "3. Exit without uploading"
read -p "Choose an option (1-3): " option

case $option in
    1)
        echo "Uploading to Test PyPI..."
        python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
        
        echo ""
        echo "Package uploaded to Test PyPI!"
        echo "To test installation, run:"
        echo "pip install --index-url https://test.pypi.org/simple/ --no-deps bolor"
        ;;
    2)
        echo "Uploading to real PyPI..."
        python3 -m twine upload dist/*
        
        echo ""
        echo "Package uploaded to PyPI!"
        echo "To install the new version, run:"
        echo "pip install --upgrade bolor"
        ;;
    *)
        echo "Exiting without uploading."
        echo "The package has been built and is available in the 'dist/' directory."
        ;;
esac

echo ""
echo "Done!"
