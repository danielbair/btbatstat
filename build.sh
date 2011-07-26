#!/bin/bash

#Remove build crap if exists
if [ -d build ] ; then 
	rm -rf build
fi
if [ -d dist ] ; then
	rm -rf dist
fi

#Build App
python setup.py py2app --iconfile BtBatStat.icns

#Zip App
cd dist
zip -r ~/Desktop/BtBatStat.zip BtBatStat.app

#Remove build crap
cd ..
rm -rf dist build
