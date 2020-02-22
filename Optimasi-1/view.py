from app import db
from app.models import Mahasiswa
from app.models import User

m = Mahasiswa.query.all()
