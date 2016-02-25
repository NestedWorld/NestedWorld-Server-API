#!/bin/sh

pip install --user -Ur requirements.txt
pip install --user -Ur requirements_dev.txt

./manage.py resetdb
./manage.py import_monsters
./manage.py import_places
