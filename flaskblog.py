from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistationForm, LoginForm
app = Flask(__name__)
# SECRET_KEY protects against modifying cookies and cross site request forgery attacks and more stuff
# app.config is how you set config values for the application
# SECRET_KEY is supposed to be a random string
app.config['SECRET_KEY'] = '6367bd0b7d25c57d19b2f68a79897059'
# Database something
# Update!: Loading the configuration for sqllite to app.cofig
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Creating the SQLAlchemy object by passing it the application
# Object contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm
# Provides a class called Model that is a declarative base which can be used to declare models
db = SQLAlchemy(app)
# reviewedusers is a table that lists the peers that have been ignored or liked
# used to recommend new users and not query 'passed' users
reviewedUser = db.Table('reviewedUser',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('reviewed_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('review_type', db.Boolean, unique=False, nullable=False)
    )

userTag = db.Table('userTag',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('tag_type', db.Boolean, unique=False, nullable=False)
    )

friendList = db.Table('friendList',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
    )

# A subclass of db.model, a declarative base that can declare models (tables)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(160), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    # Backref creates a tag column in the table.Tag 
    # 'lazy = dynamic' gives a query that we can run instead of all the data at once
    tag = db.relationship('Tag', secondary=userTag, backref=db.backref('tag_holder', lazy='dynamic'))
    friend = db.relationship('User', 
        secondary=friendList, 
        primaryjoin=id==friendList.c.user_id, 
        secondaryjoin=id==friendList.c.friend_id, 
        backref=db.backref('friendof'))
    # Column users which have allready been reviewed (liked or passed)
    rec = db.relationship('User', 
        secondary=reviewedUser, 
        primaryjoin=id==reviewedUser.c.user_id, 
        secondaryjoin=id==reviewedUser.c.reviewed_id, 
        backref=db.backref('reviewedby'))


    def  __repr__(self):
        return (f"User('{self.username}', '{self.email}', '{self.image_file}')")

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(120), unique=True, nullable=False)

    def  __repr__(self):
        return (f"Tag('{self.tagname}')")

recList = [
    {
        'name': 'Jalwan',
        'program': 'BCSI',
        'strengths': ['element_1', 'python', 'reading', 'element_4', 'element_5', 'element_6', 'element_7'],
        'weakness': ['java', 'chess', 'element_3', 'element_4', 'element_5'],
        'bio': 'This is Jalwan bio'
    },
    # {
    #     'name': 'Wilfred',
    #     'program': 'BCSI',
    #     'interests': ['cloud computing', 'gaming'],
    #     'bio': 'this is Wilfred bio'
    # }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', recList=recList)

@app.route('/about')
def about():
    return render_template('about.html', title='About')  

# The methods variable is a list of allowed methods passed to the route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistationForm()
    if form.validate_on_submit():
        # if form validates the message gets flashed, flash is a one time message
        flash(f'Account created for {form.username.data}!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'jalwan' and form.password.data == 'password':
            flash('you gave been logged in')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)

