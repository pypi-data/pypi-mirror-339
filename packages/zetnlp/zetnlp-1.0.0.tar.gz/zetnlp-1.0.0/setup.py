from setuptools import setup, find_packages

setup(
    name="zetnlp",  # Name of the package
    version="1.0.0",  # Version number
    packages=find_packages(),  # Automatically find all the packages
    install_requires=[
        "numpy",
        "nltk",  # Add any dependencies your package requires
        "spacy", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),  # Content of README
    long_description_content_type='text/markdown',
    url="https://github.com/prasenjeett/ZetNLP",
    author="Prasenjeet Howlader",
    author_email="prasenjeethowlader122@gmail.com",
    license="MIT",
)
