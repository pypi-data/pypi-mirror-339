
from setuptools import setup, find_packages

setup(
    name='parallel-brain',
    version='2.0.0',
    author='Darshan',
    description='Brain-inspired ANN with adaptive inhibition and sparse connectivity',
    packages=find_packages(),
    install_requires=[
        'torch>=1.10.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
