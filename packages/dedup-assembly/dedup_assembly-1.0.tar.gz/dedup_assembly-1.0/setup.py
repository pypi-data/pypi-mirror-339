from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'dedup_assembly',
    version = 1.0,
    author = 'Jon Doenier',
    author_email = 'doenierjon@gmail.com',
    url = 'https://github.com/doenjon/dedup',
    description = 'Deduplicate haplotigs from complex diploid genomes',
    license = "MIT license",
    packages = find_packages(),  

    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
        "plotly",
        "scipy",
        "seaborn",
        "matplotlib",
        "biopython",
        "datasketch",
        "networkx",
    ],
    entry_points={
        "console_scripts": [
            "dedup=dedup.dedup:main",
        ],
    },
)