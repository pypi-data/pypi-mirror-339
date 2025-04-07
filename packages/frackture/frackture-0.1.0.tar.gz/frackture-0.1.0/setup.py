import os
from setuptools import setup, find_packages

# Read long_description relative to setup.py's location
this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="frackture",
    version="0.1.0",
    packages=find_packages(include=["frackture", "frackture.*"]),
    install_requires=["numpy", "scipy", "scikit-learn"],
    author="GoryGrey",
    description="Frackture is a symbolic compression engine using recursive logic and entropy patterns.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
