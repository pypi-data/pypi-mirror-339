from setuptools import setup, find_packages

setup(
    name="parallel-brain",
    version="2.0.1",
    description="ParallelBrain ANN with Adaptive Inhibition - Version 3.6",
    author="Darshan",
    packages=find_packages(),
    install_requires=["torch"],
    python_requires=">=3.6",
)
