"""
Script for building the example.

Usage:
    python setup.py py2app 
"""
from setuptools import setup

DATAFILES = ['kb.png', 'mouse.png', 'no_device.png']
setup(
    app=["BtBatStat.py"],
    data_files=DATAFILES,
    options=dict(py2app=dict(
        plist=dict(
            LSUIElement=True,
        ),
    )),
    setup_requires=["py2app"],
)
