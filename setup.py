#!/usr/bin/python

from distutils.core import setup
from cloudfiles.consts import __version__

setup(
    name='oauth-dailyburn',
    version=__version__,
    description='OAuth Dailyburn',
    author='Chmouel Boudjnah',
    packages=['dailyburn']
)
