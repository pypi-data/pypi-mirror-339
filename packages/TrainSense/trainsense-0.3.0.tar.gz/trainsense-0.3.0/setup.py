# setup.py
from setuptools import setup, find_packages
import os
import re

# Function to dynamically read the version from __init__.py
def get_version(package_name):
    """Return package version as listed in `__version__` in `init.py`."""
    try:
        init_py_path = os.path.join(package_name, '__init__.py')
        with open(init_py_path, 'r', encoding='utf-8') as init_py_file:
            init_py_content = init_py_file.read()
        # Use a robust regex to find the version string
        match = re.search(r"""^__version__\s*=\s*['"]([^'"]+)['"]""", init_py_content, re.MULTILINE)
        if match:
            return match.group(1)
        raise RuntimeError(f"Unable to find __version__ string in {init_py_path}.")
    except FileNotFoundError:
        raise RuntimeError(f"Could not find {init_py_path} to read version.")
    except Exception as e:
        raise RuntimeError(f"Error reading version from {init_py_path}: {e}")


# Function to read the long description from README.md
def get_long_description(file_path="README.md"):
    """Return the contents of the README file."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(base_dir, file_path)
    try:
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using short description as long description.")
        # Provide a fallback description
        return "TrainSense: An enhanced toolkit for deep learning model analysis, profiling, and training optimization."

# Define the package name (should match the folder name)
PACKAGE_NAME = "TrainSense"

setup(
    name=PACKAGE_NAME,
    version=get_version(PACKAGE_NAME), # Dynamically read from TrainSense/__init__.py
    author="RDTvlokip", # Replace if desired
    author_email="rdtvlokip@gmail.com", # Replace with a valid contact email
    description="An enhanced toolkit for deep learning model analysis, profiling, and training optimization.",
    long_description=get_long_description(), # Read from README.md
    long_description_content_type="text/markdown", # Important for PyPI rendering
    url="https://github.com/RDTvlokip/TrainSense", # Main project URL
    project_urls={ # Additional useful links
        'Bug Tracker': 'https://github.com/RDTvlokip/TrainSense/issues',
        'Source Code': 'https://github.com/RDTvlokip/TrainSense',
        # 'Documentation': 'https://your-docs-link.com', # Add if you create separate docs
    },
    license="MIT", # Standard SPDX identifier
    license_files=('LICENSE',), # Explicitly include the LICENSE file (ensure it exists)
    packages=find_packages(exclude=["examples*", "tests*"]), # Find packages automatically, exclude examples/tests
    # Core runtime dependencies required for the package to function
    install_requires=[
        'psutil>=5.8.0',
        'torch>=1.8.0', # Maintain reasonable backward compatibility for PyTorch
        'GPUtil>=1.4.0', # For GPU monitoring features
        'matplotlib>=3.3.0' # For visualization features
    ],
    # Optional dependencies, installable via: pip install trainsense[extra_name]
    extras_require={
        'dev': [ # Dependencies helpful for development and testing
            'pytest>=6.0',      # Testing framework
            'flake8>=3.8',      # Code linting
            'black>=21.0b0',   # Code formatting
            'coverage>=5.0'    # Test coverage reporting
            ]
    },
    python_requires='>=3.7', # Specify minimum Python version compatibility
        keywords=[
        # --- Core Concepts ---
        "deep learning", "pytorch", "torch", "machine learning", "ai",
        "neural network", "model training", "optimization", "analysis",
        # --- Profiling & Performance ---
        "profiling", "performance", "profiler", "bottleneck", "latency",
        "throughput", "speed", "efficiency",
        # --- Hardware & System ---
        "gpu", "cuda", "nvidia", "monitoring", "system", "diagnostics",
        "resource management", "memory usage", "cpu usage",
        # --- Model & Training Details ---
        "architecture", "hyperparameters", "hyperparameter tuning", "hpo",
        "gradients", "gradient analysis", "vanishing gradients", "exploding gradients",
        "training stability", "debugging", "dataloader", "data loading",
        # --- Related Tools/Concepts ---
        "developer tools", "pytorch ecosystem", "mlops", "experiment tracking", # Broader terms
        "trainsense" # Include the package name itself
    ],
    # Classifiers categorize the project for PyPI: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License", # Keep this classifier for now for wider tool compatibility, despite the warning
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Typing :: Typed", # Indicates use of type hints
    ],
)