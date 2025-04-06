from setuptools import setup, find_packages

setup(
    name='hawk-sdk',
    version='0.0.13',
    packages=find_packages(),
    install_requires=[
        'google-cloud-bigquery',
        'pandas'
    ],
)
