from setuptools import setup, find_packages

setup(
    name='nullstools',
    version='0.1.1',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='darkmean',
    description=open('README.md').read(),
    url='https://github.com/darkmean-dev/nullstools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)