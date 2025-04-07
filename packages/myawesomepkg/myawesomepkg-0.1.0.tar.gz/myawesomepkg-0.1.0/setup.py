from setuptools import setup, find_packages

setup(
    name='myawesomepkg',               # Change this to your library name
    version='0.1.0',
    author='Your Name',                # Put your name here
    description='A simple greeting library',
    packages=find_packages(),
    install_requires=[],               # Add required libraries here, if any
    python_requires='>=3.6',
)
