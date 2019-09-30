from app.models import Shipmate

from app import db

jal = Shipmate(first_name="James", surname="Edgecombe", nickname="Jal")
jal.set_password("password")
db.session.add(jal)
db.session.commit()


