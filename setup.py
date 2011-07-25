"""
Script for building the example.

Usage:
    python setup.py py2app 
"""
from setuptools import setup


setup(
    app=["BtBatStat.py"],
    options=dict(py2app=dict(
        plist=dict(
            LSUIElement=True,
        ),
    )),
    setup_requires=["py2app"],
)
