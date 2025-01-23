from setuptools import setup, find_packages
from pathlib import Path
from src import __version__

# Read requirements from requirements.txt
requirements = Path("requirements.txt").read_text().splitlines()

# Read long description from README.md
long_description = Path("README.md").read_text()

setup(
    name="medspresso",
    version=__version__,
    description="Extract structured information from clinical text using local LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/medspresso",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "clinical-extract=src.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.8",
    # Include non-Python files
    package_data={
        "": [
            "configs/*.yaml",
            "prompts/*.yaml",
        ],
    },
)