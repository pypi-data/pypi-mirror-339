from setuptools import setup, find_packages

setup(
    name='py_cryptomus',
    version='0.1.1',
    author='Ted Hackwell',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    description='Python wrapper for Cryptomus API based on the requests library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

)