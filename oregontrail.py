import random

from flask import Flask, render_template, redirect, url_for
from flask_login import login_user, LoginManager, login_required
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

@login_manager.user_loader
def load_user(userid):
    return Family.query.filter(Family.id==userid).first()

db = SQLAlchemy(app)

class LoginForm(FlaskForm):
    pin = PasswordField('PIN', validators=[DataRequired()])

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    balance = db.Column(db.Integer, unique=False)
    occupation = db.Column(db.Integer, default=-1)
    pin = db.Column(db.Integer, unique=True)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(id)

    def __init__(self, name):
        self.name = name
        self.balance = 1600
        pin = random.randint(10000,99999)
        while (Family.query.filter_by(pin=pin).first() is not None): # This is really stupid
            pin = random.randint(10000,99999)
        self.pin = pin


    def __repr__(self):
        return "<%s Family>" % self.name

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        fam = Family.query.filter_by(pin=form.pin.data).first()
        if fam:
            login_user(fam)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

