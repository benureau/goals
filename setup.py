import os
from setuptools import setup

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
