from setuptools import setup, find_packages

setup(
    name="medspresso",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "llama-cpp-python>=0.2.6",
        "mlx>=0.0.8",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "huggingface-hub>=0.20.1",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'clinical-extract=src.cli:cli',
        ],
    },
) 