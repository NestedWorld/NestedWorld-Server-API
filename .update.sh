#!/bin/sh

pip install -Ur requirements.txt

./manage.py resetdb
./manage.py import_monsters
