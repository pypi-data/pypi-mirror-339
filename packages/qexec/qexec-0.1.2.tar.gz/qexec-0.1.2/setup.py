from setuptools import setup, find_packages
import os

setup(
    name="qexec",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "cryptography",  # Required by qexec for encryption
    ],
    author="Kiko",
    author_email="your.email@example.com",
    description="A package for executing commands through AI using qexec",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qexec-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)