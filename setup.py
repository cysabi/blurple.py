from setuptools import setup, find_packages
import os


version = os.getenv("VERSION").split("/")[-1][1:]
name = os.getenv("NAME")


with open('requirements.txt') as file:
    requirements = file.read().splitlines()


with open('README.md') as file:
    readme = file.read()


kwargs = {
    "author": 'LeptoFlare',
    "url": 'https://github.com/LeptoFlare/blurple.py',
    "project_urls": {
        "Issues": "https://github.com/LeptoFlare/blurple.py/issues",
        "Docs": "https://lepto.tech/blurple.py",
    },
    "version": version,
    "packages": find_packages(),
    "license": 'MIT',
    "description": 'A front-end framework for discord.py',
    "long_description": readme,
    "long_description_content_type": "text/markdown",
    "include_package_data": True,
    "install_requires": requirements,
    "classifiers": [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
}


setup(name=name, **kwargs)
