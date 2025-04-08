from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='MDRMF',
    version='0.0.13',
    packages=find_packages(),
    description='Multidrug Resistance Machine Fishing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jacob Molin Nielsen',
    author_email='jacob.molin@me.com',
    url='https://github.com/MolinDiscovery/MDRMF',  # use the URL to the github repo
    keywords=['machine fishing', 'drug discovery', 'machine learning', 'pool based active learning'],
    classifiers=[],
    include_package_data=True,
    package_data={
        'MDRMF': ['schemas/*.yaml'],
    },
    install_requires=[
        'joblib',
        'lightgbm',
        'matplotlib',
        'numpy',
        'pandas',
        'pykwalify',
        'pyyaml',
        'rdkit',
        'scipy',
        'scikit-learn'
    ],    
)