
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Plane",
    version = "0.0.1",
    author = "Chris Perivolaropoulos",
    author_email = "darksaga2006@gmail.com",
    description = ("Relate abstract data togetherin a fuzzy way."),
    license = "GPL",
    keywords = "",
    url = "http://packages.python.org/Plane",
    packages=['plane', 'plane.test'],
    install_requires=[],
    tests_require=['nose'],
    long_description=read('README.org'),
    test_suite='plane.test',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    ],
)
