from setuptools import setup, find_packages

setup(
    name="the-judge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    author="Luis",
    author_email="luisbeqjamw@gmail.com",
    description="A library for evaluating LLM responses using various metrics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luisbeqja/the-judge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 