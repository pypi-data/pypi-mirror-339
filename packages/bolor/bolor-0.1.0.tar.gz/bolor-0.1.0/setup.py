from setuptools import setup, find_packages

setup(
    name="bolor",
    version="0.1.0",
    description="Local LLM-based code repair tool with self-healing capabilities",
    author="Bolor Project",
    author_email="info@bolorproject.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "ctransformers>=0.2.0",  # For local LLM
        "langchain>=0.0.208",    # For embeddings and chains
        "chromadb>=0.4.0",       # Vector storage
        "rich>=13.0.0",          # Terminal UI
        "astunparse>=1.6.3",     # Python AST manipulation
        "typer>=0.9.0",         # Modern CLI interface
        "pytest>=7.0.0",        # For testing fixes
    ],
    entry_points={
        "console_scripts": [
            "bolor=bolor.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
