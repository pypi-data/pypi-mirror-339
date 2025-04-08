from setuptools import setup, find_packages

setup(
    name='my_unique_sample_package',  # Must be globally unique on PyPI
    version='0.1.0',
    description='A cool package that greets users with fun',
    author='Venky',
    author_email='your_email@example.com',
    packages=find_packages(),
    install_requires=[],  # List dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)