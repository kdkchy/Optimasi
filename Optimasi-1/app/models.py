from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    nim = db.Column(db.String(9), index=True, unique=True)
    senin_a = db.Column(db.String(3))
    senin_b = db.Column(db.String(3))
    senin_d = db.Column(db.String(3))
    senin_e = db.Column(db.String(3))
    selasa_a = db.Column(db.String(3))
    selasa_b = db.Column(db.String(3))
    selasa_d = db.Column(db.String(3))
    selasa_e = db.Column(db.String(3))
    rabu_a = db.Column(db.String(3))
    rabu_b = db.Column(db.String(3))
    rabu_d = db.Column(db.String(3))
    rabu_e = db.Column(db.String(3))
    kamis_a = db.Column(db.String(3))
    kamis_b = db.Column(db.String(3))
    kamis_d = db.Column(db.String(3))
    kamis_e = db.Column(db.String(3))
    jumat_a = db.Column(db.String(3))
    jumat_b = db.Column(db.String(3))
    jumat_d = db.Column(db.String(3))
    jumat_f = db.Column(db.String(3))

    def __repr__(self):
        return '<Mahasiswa {}>'.format(self.nama)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))