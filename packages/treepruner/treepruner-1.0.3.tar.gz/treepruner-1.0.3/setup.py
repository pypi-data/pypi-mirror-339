from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="treepruner",
    version="1.0.3",
    description="A package for pruning phylogenetic trees",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hegedani/Pruning_algorithms_for_phylogenetic_trees",
    author="Dániel Hegedűs, Márk Hunor Juhász",
    author_email="markh.shepherd@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["ete3>=3.1.3", "numpy>=2.2.3", "matplotlib>=3.10.0", "six>=1.17.0"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10, <3.13",
)
