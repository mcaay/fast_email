from setuptools import setup, find_packages

description = """\
High level email package made to send single or multiple emails \
in just 2 lines of code (including the import statement).\
"""

with open("README.md", 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="fast_email",
    version="0.1.1",
    author="Konrad Olszowski",
    author_email="olszowski.konrad@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcaay/fast_email",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
