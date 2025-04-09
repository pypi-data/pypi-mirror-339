from setuptools import setup, find_packages

setup(
    name='parallel-brain',
    version='2.0.3',
    author='Darshan U P',
    author_email='darshandileep4@gmail.com',
    description='ParallelBrain ANN with Adaptive Inhibition and Sparse Connectivity',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/parallel-brain',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
