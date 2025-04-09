from setuptools import setup, find_packages
import pathlib

this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="lockprompt",
    version="1.1.2",
    description="Lightweight safety layer to scan prompts and LLM outputs via external API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Willis-Owen",
    author_email="david@willis-owen.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)
