#!/bin/sh

pip install --user -Ur requirements.txt

./manage.py resetdb
./manage.py import_monsters
./manage.py import_places
