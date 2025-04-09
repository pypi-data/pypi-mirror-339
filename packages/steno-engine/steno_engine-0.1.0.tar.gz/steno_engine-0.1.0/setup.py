from setuptools import setup, find_packages

setup(
    name="steno-python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy",
        "onnxruntime",
        "transformers"
    ],
    entry_points={
        "console_scripts": [
            "steno=steno.main:cli"
        ]
    },
    python_requires=">=3.8",
    author="Greg Lamp",
    description="Tokenator",
)

