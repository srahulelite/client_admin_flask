from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a flask instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Secret Key
app.config['SECRET_KEY'] = "slakfj9*&^&*%98"

# Initialize Database
db = SQLAlchemy(app)


############### DATABASE THINGS ####################
#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a String
    def __repr__(self):
        return '<Name %r >' % self.name
    
############### DATABASE THINGS ####################

# Create UserForm Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create form Class
class Namerform(FlaskForm):
    name = StringField("What's your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")

#localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    return render_template("add_user.html")

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = Namerform()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html", 
                           name = name, 
                           form = form)
