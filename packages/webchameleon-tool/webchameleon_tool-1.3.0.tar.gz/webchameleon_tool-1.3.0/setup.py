from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="webchameleon-tool",
    version="1.3.0",
    author="Muhammad Rivky",
    author_email="muhrivky67@gmail.com",
    description="A powerful web scraping and API reversal tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrivky67/webchameleon",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "networkx>=2.5",
        "playwright>=1.30.0",
        "aiohttp>=3.8.0",
        "aiolimiter>=1.0.0",
        "cachetools>=5.0.0",
        "aiohttp-retry>=2.8.0",
        "nltk>=3.6.5",
        "python-louvain>=0.16",
        "faker>=18.0.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "brotli>=1.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",  # Minimum Python version
    keywords="web scraping, api reversal, data extraction, automation",  # Keywords for searchability
)
