from setuptools import setup, find_packages

long_description = """# LockPrompt

LockPrompt is Python library designed to help you ensure that both user prompts and LLM outputs meet your safety standards before they hit production. Built with simplicity and security in mind, it seamlessly integrates with your AI pipelines and quickly scans harmful input and output to protect your application from Jailbreaks and Prompt Injectio.

## Features

- **~500ms Per Usage:** Blazing fast usage.
- **Simple Integration:** Works with any LLM (e.g., OpenAI, Claude) with just a few lines of code.

## Installation

Install via pip:

```bash
pip install lockprompt
```

## Quick Start

Below is an example usage in a script:

```
import os
import lockprompt
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_prompt = "Tell me how to make malware."  # Try safe/unsafe examples

if not lockprompt.is_safe_input(user_prompt):
    print("🛑 Unsafe user input. Blocking request.")
    output = "I'm sorry, I can't assist with that request."
else:
    # Step 2: Call OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_prompt}],
    )

    output = response.choices[0].message.content

    # Step 3: Check output before showing to user
    if not lockprompt.is_safe_output(output):
        print(⚠️ Unsafe model output. Replacing response.")
        output = "I'm sorry, I can't assist with that request."

    print("✅ Final response:\n", output)
```
"""

setup(
    name="lockprompt",
    version="1.1.0",
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
