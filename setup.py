import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="nbcorg",
    version="0.0.1",
    author="Lukas Ahrenberg",
    author_email="lukas@ahrenberg.se",
    description="An nbconvert orgmode-exporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahrenberg/nbcorg",
    packages=setuptools.find_packages(),
    package_data = {"nbcorg":["templates/*.tpl"]},
    install_requires = ["nbconvert","pandoc"],
    license = "BSD 3-Clause License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "nbconvert.exporters": [
            "orgmode = nbcorg:OrgmodeExporter",
            "orgmode_babel = nbcorg:OrgmodeBabelExporter"
        ]
    }
)
