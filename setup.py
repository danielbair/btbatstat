"""
Script for building the example.

Usage:
    python setup.py py2app 
"""
from setuptools import setup

DATAFILES = ['icons', 'BtBatStat.icns']
setup(
    app=["BtBatStat.py"],
    data_files=DATAFILES,
    options=dict(py2app=dict(
        plist=dict(
            LSUIElement=True,
	    CFBundleShortVersionString="0.6",
	    CFBundleVersion="0.6",
	    CFBundleIconFile="BtBatStat.icns",
	    CFBundleIdentifier="org.vandalon.BtBatStat",
	    NSHumanReadableCopyright="Joris Vandalon",
        ),
    )),
    setup_requires=["py2app"],
)
