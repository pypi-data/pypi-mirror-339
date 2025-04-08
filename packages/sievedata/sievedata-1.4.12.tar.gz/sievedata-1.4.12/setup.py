from setuptools import setup, find_packages

VERSION = "1.4.12"

f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="sievedata",
    version=VERSION,
    description="Sieve CLI and Python Client",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Sieve Team",
    author_email="developer@sievedata.com",
    url="https://github.com/sieve-data/sieve",
    license="unlicensed",
    packages=find_packages(exclude=["ez_setup", "tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.0,<3.0",
        "click>=8.0,<9.0",
        "pydantic>=2.0,<3.0",
        "pathlib>=1.0.1,<2.0",
        "tqdm>=4.64.1,<5.0",
        "networkx>=3.0,<4.0.0",
        "typeguard>=4.0.0,<5.0.0",
        "typer>=0.7.0,<1.0.0",
        "rich>=13.0.0,<14.0.0",
        "cloudpickle>=3.0.0,<4.0.0",
        "docstring_parser>=0.16.0,<1.0.0",
        "jsonref>=1.0.0,<2.0.0",
        "protobuf>=3.10.0,<5.0.0",
        "pyyaml>=6.0.0,<7.0.0",
        "grpcio>=1.60.0,<2.0.0",
        "sseclient>=0.0.20,<1.0.0",
        "python-dateutil>=2.8.0,<3.0.0",
        "pathspec>=0.12,<1.0",
    ],
    entry_points={
        "console_scripts": [
            "sieve = sieve._cli.sieve:start_cli",
        ]
    },
)
