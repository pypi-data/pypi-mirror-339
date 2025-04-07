from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oratools",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "pytube>=15.0.0",
        "rich>=14.0.0",
        "requests>=2.30.0",
        "pillow>=11.0.0",
        "pyfiglet>=1.0.2",
        "psutil>=5.9.5",
        "dnspython>=2.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.1.0",
            "responses>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "oratools=oratools.cli:main",
        ],
    },
    author="Owen Orcan",
    author_email="owenorcan@gmail.com",
    description="A collection of essential developer utilities in a single CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/owenorcan/oratools",
    project_urls={
        "Source Code": "https://github.com/owenorcan/oratools",
    },
    keywords="cli, developer-tools, youtube-downloader, system-info, network-tools, file-search, utilities",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
) 