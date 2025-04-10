from setuptools import setup, find_packages

setup(
    name="orly",
    version="0.1.0",
    author="Zarby",
    author_email="",
    description="This allows you to load modules in an elegant way.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zZarby/orly",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
