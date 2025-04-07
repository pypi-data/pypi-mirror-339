from setuptools import setup, find_packages

setup(
    name="quantum-machine",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "quantum=quantum.main:app"
        ]
    },
    author="Nitinkumar Suvagiya",
    author_email="itsupport@quantumdatalytica.com",
    description="Quantum CLI for running Quantum Machines",
    long_description="**Quantum** is a command-line tool developed by QuantumDatalytica LLC for building, running, testing, and managing modular \"Quantum Machines\" in a distributed data analytics pipeline.",
    long_description_content_type="text/markdown",
    url="https://github.com/QuantumDatalytica-LLC/quantum-cli.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)