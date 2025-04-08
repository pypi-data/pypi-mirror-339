from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gads3client",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={},
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="An async and lightweight S3 client for uploading, downloading, and deleting files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gads3client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)