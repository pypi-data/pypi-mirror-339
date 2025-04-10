from setuptools import setup, find_packages
setup(
name='pydentate',
version='1.0.0',
author='Jacob Toney',
author_email='jwt@mit.edu',
description='Graph Neural Networks for Predicting Metal-Ligand Coordination in Transition Metal Complexes',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.10, <3.13',
)


