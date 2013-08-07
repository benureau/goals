import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "goals",
    version = "0.95",
    author = "Fabien Benureau",
    author_email = "fabien.benureau@inria.fr",
    description = ("Intrinsic-motivation algorithms"),
    license = "Not Yet Decided.",
    keywords = "instrinsic-motivation goal-oriented",
    url = "flowers.inria.fr",
    packages=['goals', 'goals.gfx',
                       'goals.explorer',
                       'goals.explorer.motor',
                       'goals.explorer.effect',
                       'goals.explorer.tools',],
    #long_description=read('README'),
    classifiers=[],
)
