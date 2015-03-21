from setuptools import setup, find_packages
from os.path import join

NAME = "ubiety"
DESCRIPTION = "An IP/Mac presence checker."
AUTHOR = "Frank Lazzarini"
AUTHOR_EMAIL = "flazzarini@gmail.com"
VERSION = open(join(NAME, 'version.txt')).read().strip()
LONG_DESCRIPTION = open("README.rst").read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Private",
    include_package_data=True,
    install_requires=[
        'config_resolver',
        'bottle'
    ],
    entry_points={
        'console_scripts': []
    },
    dependency_links=[],
    packages=find_packages(exclude=["tests.*", "tests"]),
    zip_safe=False,
)
