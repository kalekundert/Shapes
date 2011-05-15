#!/usr/bin/env bash

python setup.py build
su -c "python setup.py install"
