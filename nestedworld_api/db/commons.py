from nestedworld_api.db import db

elements = db.Enum('water', 'fire', 'earth', 'electric', 'plant', name='element_type')
