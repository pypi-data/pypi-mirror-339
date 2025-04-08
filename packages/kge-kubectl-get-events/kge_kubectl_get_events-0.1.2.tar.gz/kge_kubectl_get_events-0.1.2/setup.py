from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kge-kubectl-get-events",
    version="0.1.2",
    author="Jesse",
    author_email="",  # Add your email here
    description="A kubectl plugin for viewing Kubernetes events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jesse/kge-kubectl-get-events",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "kubernetes>=12.0.0",
    ],
    entry_points={
        "console_scripts": [
            "kge=kge.cli.main:main",
        ],
    },
) 