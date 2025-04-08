from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tokenaligner",
    version="0.1.1",
    author="Yatin Chaudhary",
    author_email="yatinchaudhary91@gmail.com",
    description="A lightweight utility to align NER labels with tokenized input for HuggingFace models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YatinChaudhary/tokenaligner",
    packages=find_packages(),
    install_requires=[
        "datasets>=2.0.0",
        "transformers>=4.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)