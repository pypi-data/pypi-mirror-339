from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pds3_utils',
    version='0.1',
    author='Mark S. Bentley',
    author_email='mark@lunartech.org',
    description='A set of utilities to analyse PDS3 meta-data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msbentley/pds3_utils",
    download_url = 'https://github.com/msbentley/pds3_utils/archive/0.1.tar.gz',
    install_requires=['pandas','pyyaml','pvl'],
    python_requires='>=3.0',
    keywords = ['PDS','PDS3','planetary'],
    zip_safe=False)
