"""
Script for building the example.

Usage:
    python setup.py py2app 
"""
from setuptools import setup

DATAFILES = ['kb.png', 'mouse.png', 'TrackpadIcon.png', 'no_device.png', 'BtBatStat.icns']
setup(
    app=["BtBatStat.py"],
    data_files=DATAFILES,
    options=dict(py2app=dict(
        plist=dict(
            LSUIElement=True,
	    CFBundleShortVersionString="0.5",
	    CFBundleVersion="0.5",
	    CFBundleIconFile="BtBatStat.icns",
	    CFBundleIdentifier="org.vandalon.BtBatStat",
	    NSHumanReadableCopyright="Joris Vandalon",
        ),
    )),
    setup_requires=["py2app"],
)
