import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openbiolink",
    version="0.1.3",
    author="Anna Breit, Matthias Samwald, Simon Ott, Laura Graf, Asan Agibetov",
    author_email="matthiassamwald@gmail.com",
    description="A framework for the OpenBioLink knowledge graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenBioLink/OpenBioLink",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click",
        "numpy",
        "pandas>=0.23.4",
        "tqdm>=4.29.1",
        "torch"
    ],
    extras_require={
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
            "sphinx-click",
            "sphinx-autodoc-typehints",
            "sphinx_automodapi",
            "texext",
        ]
    },
    python_requires=">=3.6",
    entry_points={"console_scripts": ["openbiolink = openbiolink.openBioLink:main", ], },
)
