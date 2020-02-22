from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app.models import Mahasiswa

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InputForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    nim = StringField('Nim', validators=[DataRequired()])
    senin_a = StringField('Senin - 08.00', validators=[DataRequired()])
    senin_b = StringField('Senin - 10.00', validators=[DataRequired()])
    senin_d = StringField('Senin - 13.00', validators=[DataRequired()])
    senin_e = StringField('Senin - 15.00', validators=[DataRequired()])
    selasa_a = StringField('Selasa - 08.00', validators=[DataRequired()])
    selasa_b = StringField('Selasa - 10.00', validators=[DataRequired()])
    selasa_d = StringField('Selasa - 13.00', validators=[DataRequired()])
    selasa_e = StringField('Selasa - 15.00', validators=[DataRequired()])
    rabu_a = StringField('Rabu - 08.00', validators=[DataRequired()])
    rabu_b = StringField('Rabu - 10.00', validators=[DataRequired()])
    rabu_d = StringField('Rabu - 13.00', validators=[DataRequired()])
    rabu_e = StringField('Rabu - 15.00', validators=[DataRequired()])
    kamis_a = StringField('Kamis - 08.00', validators=[DataRequired()])
    kamis_b = StringField('Kamis - 10.00', validators=[DataRequired()])
    kamis_d = StringField('Kamis - 13.00', validators=[DataRequired()])
    kamis_e = StringField('Kamis - 15.00', validators=[DataRequired()])
    jumat_a = StringField('Jumat - 08.00', validators=[DataRequired()])
    jumat_b = StringField('Jumat - 10.00', validators=[DataRequired()])
    jumat_d = StringField('Jumat - 13.00', validators=[DataRequired()])
    jumat_f = StringField('Jumat - 15.00', validators=[DataRequired()])
    submit = SubmitField('Tambah')

    def validate_nim(self, nim):
        mahasiswa = Mahasiswa.query.filter_by(nim=nim.data).first()
        if mahasiswa is not None:
            raise ValidationError('Please use a different NIM.')