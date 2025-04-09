from setuptools import setup, find_packages

setup(
    name="abp-tools",
    version="0.1",
    description="ABP is an encryption algorithm.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Genius_um",
    python_requires=">=3.9",
    url="https://github.com/Geniusum/abp",
    packages=find_packages(),#["abp"], # find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
