from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="toxolib",
    version="0.1.2",
    author="Dhruvil Chodvadiya",
    author_email="your.email@example.com",
    description="A tool for metagenomic taxonomic profiling and abundance matrix generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhruvac29/toxolib",
    packages=find_packages(include=['toxolib', 'toxolib.*']),
    package_data={
        'toxolib': ['data/*', 'data/environment.yml'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "scikit-bio>=0.5.0",
        "matplotlib",
        "seaborn",
        "paramiko>=2.7.0",  # For SSH connections to HPC
        "pyyaml>=5.1",     # For configuration files
    ],
    entry_points={
        "console_scripts": [
            "toxolib=toxolib.cli:main",
        ],
    },
)
