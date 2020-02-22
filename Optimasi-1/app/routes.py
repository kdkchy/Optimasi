from flask import render_template
from app import app
from app.forms  import LoginForm
from flask import render_template, flash, redirect
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.models import User
from app.models import Mahasiswa
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import InputForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    data = Mahasiswa.query.all()
    return render_template("index.html", title='Home Page', data=data)

@app.route('/test')
def test():
    user = 'Kaltara'
    return render_template('test.html', title='Test', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/rancang')
@login_required
def rancang():
    return render_template('rancang.html', title='Rancang')

@app.route('/inputMahasiswa', methods=['GET', 'POST'])
@login_required
def inputMahasiswa():
    form = InputForm()
    if form.validate_on_submit():
        mahasiswa = Mahasiswa(nama=form.nama.data, nim=form.nim.data, senin_a=form.senin_a.data+('11'), senin_b=form.senin_b.data+('12'), senin_d=form.senin_d.data+('13'), senin_e=form.senin_e.data+('14'),
        selasa_a=form.selasa_a.data+('21'), selasa_b=form.selasa_b.data+('22'), selasa_d=form.selasa_d.data+('23'), selasa_e=form.selasa_e.data+('24'),
        rabu_a=form.rabu_a.data+('31'), rabu_b=form.rabu_b.data+('32'), rabu_d=form.rabu_d.data+('33'), rabu_e=form.rabu_e.data+('34'),
        kamis_a=form.kamis_a.data+('41'), kamis_b=form.kamis_b.data+('42'), kamis_d=form.kamis_d.data+('43'), kamis_e=form.kamis_e.data+('44'),
        jumat_a=form.jumat_a.data+('51'), jumat_b=form.jumat_b.data+('52'), jumat_d=form.jumat_d.data+('53'), jumat_f=form.jumat_f.data+('54'))
        db.session.add(mahasiswa)
        db.session.commit()
        flash('Congratulations, data sudah masuk!')
        return redirect(url_for('inputMahasiswa'))
    return render_template('inputMahasiswa.html', title='Input Jadwal Mahasiswa', form=form)

@app.route('/inputDosen', methods=['GET', 'POST'])
@login_required
def inputDosen():
    form = InputForm()
    if form.validate_on_submit():
        mahasiswa = Mahasiswa(nama=form.nama.data, nim=form.nim.data, senin_a=form.senin_a.data+('11'), senin_b=form.senin_b.data+('12'), senin_d=form.senin_d.data+('13'), senin_e=form.senin_e.data+('14'),
        selasa_a=form.selasa_a.data+('21'), selasa_b=form.selasa_b.data+('22'), selasa_d=form.selasa_d.data+('23'), selasa_e=form.selasa_e.data+('24'),
        rabu_a=form.rabu_a.data+('31'), rabu_b=form.rabu_b.data+('32'), rabu_d=form.rabu_d.data+('33'), rabu_e=form.rabu_e.data+('34'),
        kamis_a=form.kamis_a.data+('41'), kamis_b=form.kamis_b.data+('42'), kamis_d=form.kamis_d.data+('43'), kamis_e=form.kamis_e.data+('44'),
        jumat_a=form.jumat_a.data+('51'), jumat_b=form.jumat_b.data+('52'), jumat_d=form.jumat_d.data+('53'), jumat_f=form.jumat_f.data+('54'))
        db.session.add(mahasiswa)
        db.session.commit()
        flash('Congratulations, data sudah masuk!')
        return redirect(url_for('inputDosen'))
    return render_template('inputDosen.html', title='Input Jadwal Mahasiswa', form=form)

def factors(num):
  return [x for x in range(1, num+1) if num%x==0]

def bbb(a):
    return a+2

@app.route('/factors/<int:num>')
def factors_route(num):
  return "The factors of {} are {}".format(num, factors(num))

@app.route('/stringa/<int:a>')
def aaa(a):
    return "The factors of "+str(bbb(a))