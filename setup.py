import sys
from setuptools import setup, find_packages


# Load all requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


# Python version
python_version = sys.version.split(' ')[0]

setup(
    name='article_models_library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=f'>={python_version}',
)
