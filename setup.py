import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytomproject",
    version="0.3.2",
    author="Luis Gracia",
    author_email="luisgracia@phoxspark.com",
    description="BSC Python Practice for Bioinformatics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhoxSpark/pytom-project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
