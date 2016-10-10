#!/bin/sh

pip install --user -Ur requirements.txt
pip install --user -Ur requirements_dev.txt

./manage.py db reset
./manage.py db import_monsters
./manage.py db import_attacks
./manage.py db import_places
./manage.py db import_objects
