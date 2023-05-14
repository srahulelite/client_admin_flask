from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


# Create a flask instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Secret Key
app.config['SECRET_KEY'] = "slakfj9*&^&*%98"

# Initialize Database
db = SQLAlchemy(app)

# Migration Configuration
migrate = Migrate(app, db)



############### DATABASE THINGS ##################
#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    fav_color = db.Column(db.String(100), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a String
    def __repr__(self):
        return '<Name %r >' % self.name

####################################################    

############## Form Classes #################

# Create UserForm Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    fav_color = StringField("Favourite Color")
    submit = SubmitField("Submit")

# Create form Class
class Namerform(FlaskForm):
    name = StringField("What's your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#############################################


# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")

#localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)


# Add User
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, fav_color=form.fav_color.data)
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.email.data = ''
            form.fav_color.data = ''
            flash("User Added Successfully")
        else:
            flash(form.email.data + " already registered !! Please try again")
            form.name.data = ''
            form.email.data = ''
            form.fav_color.data = ''
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", form=form, our_users=our_users)


# Update User Details
@app.route('/update/<id>', methods=['GET', 'POST'])
def update_user(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.fav_color = request.form['fav_color']
        db.session.commit()
        flash("User Updated Successfully ")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form=form, our_users = our_users)
    else:
        return render_template("update_user.html",form=form, name_to_update = name_to_update)
    
# Delete User
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User Deleted Successfully")
    form = UserForm()
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form, our_users = our_users)




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


############## Errors ###############
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

############## Errors ###############