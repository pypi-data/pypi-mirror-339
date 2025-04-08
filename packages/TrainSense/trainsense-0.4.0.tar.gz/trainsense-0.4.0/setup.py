# setup.py
from setuptools import setup, find_packages
import os
import re
import sys

# --- Helper Functions ---

def get_version(package_name):
    """Return package version as listed in `__version__` in `init.py`."""
    try:
        init_py_path = os.path.join(package_name, '__init__.py')
        with open(init_py_path, 'r', encoding='utf-8') as init_py_file:
            init_py_content = init_py_file.read()
        match = re.search(r"""^__version__\s*=\s*['"]([^'"]+)['"]""", init_py_content, re.MULTILINE)
        if match:
            return match.group(1)
        raise RuntimeError(f"Unable to find __version__ string in {init_py_path}.")
    except FileNotFoundError:
        raise RuntimeError(f"Could not find {init_py_path} to read version.")
    except Exception as e:
        raise RuntimeError(f"Error reading version from {init_py_path}: {e}")

def get_long_description(file_path="README.md"):
    """Return the contents of the README file."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(base_dir, file_path)
    if not os.path.exists(readme_path):
        print(f"WARNING: {file_path} not found. Using short description only.", file=sys.stderr)
        return "TrainSense: Toolkit for PyTorch analysis, profiling, and optimization." # Short fallback
    try:
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"WARNING: Could not read {file_path}: {e}", file=sys.stderr)
        return "TrainSense: Toolkit for PyTorch analysis, profiling, and optimization." # Short fallback

# --- Package Definition ---

PACKAGE_NAME = "TrainSense"
VERSION = get_version(PACKAGE_NAME) # Read version once

# Core dependencies - absolutely required to run the main features
CORE_DEPS = [
    'psutil>=5.8.0',
    'torch>=1.8.0', # Keep a reasonable minimum PyTorch version
    'GPUtil>=1.4.0' # For GPU monitoring features
]

# Optional dependencies grouped by feature
EXTRAS_DEPS = {
    'plotting': ['matplotlib>=3.3.0', 'numpy'], # Added numpy as it's often needed with matplotlib
    'html': ['jinja2>=3.0.0'], # For HTML report generation
    'trl': ['transformers>=4.0.0'], # For TRL Callback integration (adjust version as needed)
    'dev': [ # Dependencies for development and testing
        'pytest>=6.0',
        'flake8>=3.8',
        'black>=21.0b0',
        'coverage>=5.0',
        'mypy>=0.900', # Optional: Static type checking
        'ipykernel', # For notebooks if used in dev
    ]
}

# Create an 'all' extra that includes plotting and html
EXTRAS_DEPS['all'] = EXTRAS_DEPS['plotting'] + EXTRAS_DEPS['html'] + EXTRAS_DEPS['trl']

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="RDTvlokip",
    author_email="rdtvlokip@gmail.com", # Consider using a project-specific email if public
    description="Toolkit for PyTorch model analysis, profiling, and training optimization.", # Slightly shorter
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/RDTvlokip/TrainSense",
    project_urls={
        'Bug Tracker': 'https://github.com/RDTvlokip/TrainSense/issues',
        'Source Code': 'https://github.com/RDTvlokip/TrainSense',
        # 'Documentation': f'https://{PACKAGE_NAME}.readthedocs.io/en/latest/', # Example if using ReadTheDocs
    },
    license="MIT",
    license_files=('LICENSE',), # Assumes LICENSE file exists at the root
    packages=find_packages(exclude=["tests*", "examples*"]), # Exclude tests and examples folders
    install_requires=CORE_DEPS, # List only core dependencies here
    extras_require=EXTRAS_DEPS, # Define optional dependencies
    python_requires='>=3.7', # Minimum Python version
    keywords=[
        "pytorch", "torch", "deep learning", "machine learning", "ai",
        "profiling", "profiler", "performance", "optimization", "analysis",
        "diagnostics", "monitoring", "gpu", "cuda", "nvidia", "memory usage",
        "gradients", "training", "debugging", "developer tools", "mlops",
        "hyperparameters", "dataloader", "trainsense" # Include package name
    ],
    # Entry points for potential future CLI tools
    # entry_points={
    #     'console_scripts': [
    #         'trainsense-analyze=TrainSense.cli:main_analyze', # Example entry point
    #     ],
    # },
    classifiers=[
        # More specific Development Status if applicable (e.g., 5 - Production/Stable)
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License", # Standard classifier for MIT
        "Operating System :: OS Independent", # Should work on Win, macOS, Linux
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
        "Topic :: Utilities", # Fits the "toolkit" nature
        "Typing :: Typed",
    ],
)