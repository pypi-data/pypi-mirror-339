from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="synthdef-parser",
    version="0.1.0",
    packages=find_packages(),
    description="A parser for SuperCollider SynthDef binary files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rexmalebka",
    author_email="rexmalebka@krutt.org",
    license="MIT",
    python_requires=">=3.7",

)
