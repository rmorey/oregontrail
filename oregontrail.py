from enum import Enum

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

STARTING_BALANCE = 1600
BANKER_BONUS = 500

# Occupations
BANKER = 1 # +$500
FARMER = 2 # + 10 food
TEACHER = 3 # + 10 free hints
DOCTOR = 4 # + 3 cures

@login_manager.user_loader
def load_user(userid):
    return Family.query.filter_by(id=int(userid)).first()

class LoginForm(FlaskForm):
    pin = PasswordField('PIN', validators=[DataRequired()])

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    balance = db.Column(db.Integer, default = 0)
    occupation = db.Column(db.Integer)
    food = db.Column(db.Integer, default=0)
    clothes = db.Column(db.Integer, default=0)
    wheels = db.Column(db.Integer, default=0)
    penicillin = db.Column(db.Integer, default=0)
    salts = db.Column(db.Integer, default=0)
    ox = db.Column(db.Integer, default=0)


    pin = db.Column(db.Integer, unique=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, name, pin, balance, food=0, clothes=0, wheels=0, ox=0, salts=0, penicillin=0):
        self.name = name
        self.pin = pin
        self.food = food
        self.clothes = clothes
        self.wheels = wheels
        self.ox = ox
        self.salts = salts
        self.balance = balance
        self.penicillin = penicillin

    def give_occupation(self, occupation):
        self.occupation = occupation
        if occupation == BANKER:
            self.balance += BANKER_BONUS
        if occupation == FARMER:
            self.food += 10
        

    def __repr__(self):
        return "<%s Family>" % self.name

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        fam = Family.query.filter_by(pin=form.pin.data).first()
        if fam:
            print("correct credentials")
            if login_user(fam):
                print('Logged in successfully.')
                print(current_user)
                return redirect(url_for('home'))
        else:
      
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/home", methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

