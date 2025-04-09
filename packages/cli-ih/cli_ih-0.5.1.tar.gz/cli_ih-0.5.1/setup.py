from setuptools import setup, find_packages


setup(
    name="cli_ih",
    version = "0.5.1",
    packages=find_packages(),
    install_requires = [
        'logging==0.4.9.6'
    ]
)