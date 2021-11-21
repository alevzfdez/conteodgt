#! /bin/bash

cd src
python2.7 setup.py build_ext --inplace
mv *.so cythonf/
