from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="openf5-utils",
    description="Utilities for OpenF5 TTS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="mrfakename",
    author_email="me@mrfake.name",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    url="https://github.com/fakerybakery/openf5-utils",
)