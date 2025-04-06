from setuptools import setup, find_packages

setup(
    name="lockprompt",
    version="0.1.3",
    description="Lightweight safety layer to scan prompts and LLM outputs via external API.",
    author="David Willis-Owen",
    author_email="david@willis-owen.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)
