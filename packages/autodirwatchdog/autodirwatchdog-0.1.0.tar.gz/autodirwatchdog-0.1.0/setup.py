from setuptools import setup, find_packages

setup(
    name='autodirwatchdog',
    version='0.1.0',
    description='Automatically watch a folder and process files (rename and move).',
    author='Venky',
    author_email='your_email@example.com',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
