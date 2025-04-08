from setuptools import setup, find_packages

setup(
    name="mAbLab",
    version="1.0.0",
    author="Paul",
    author_email="paul@example.com",
    description="A library for analyzing monoclonal antibody characteristics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mAbLab",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "antpack==0.3.6.1",
        "biopython==1.84",
        "numpy==2.1.3",
        "Levenshtein==0.26.1",
        # Add other dependencies as needed
    ],
)
