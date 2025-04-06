from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ia-manager",
    version="1.0.1",
    author="vichmartins",
    description="A Python package to scrape and download files from the Internet Archive.",  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",  # Format of the long description
    url="https://github.com/vichmartins/internet-archive-downloader",
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose a license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Minimum Python version required
    install_requires=[  # List of dependencies directly defined here
        "requests>=2.26.0",
        "beautifulsoup4>=4.10.0",
        "tqdm>=4.62.0",
    ],
    entry_points={  # Define the command-line interface
        "console_scripts": [
            "iadl=iadl.cli:main",  # Command: ias -> calls main() in ias.cli
            "iadl-cleanup=iadl.scripts.uninstall:main",  # Uninstall script
        ],
    },
)