from datetime import datetime
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(50), nullable=False, default='pic.jpg')
    email = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, '{self.email}', '{self.image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Lisandro Guerra',
        'title': 'Post 1',
        'content': 'Python Programing',
        'date_posted': 'April 08, 2022'
    },
    {
        'author': 'Maria Moreira',
        'title': 'Post 2',
        'content': 'Human Resources',
        'date_posted': 'February 05, 2022'
    },
    {
        'author': 'Lisandra S Pires',
        'title': 'Post 3',
        'content': 'Graphos Theory',
        'date_posted': 'September 30, 2022'
    },
    {
        'author': 'Anita G S Pires',
        'title': 'Post 4',
        'content': 'Jewelery tips',
        'date_posted': 'November 14, 2022'
    },
    {
        'author': 'Lisandro Guerra',
        'title': 'Post 5',
        'content': 'Software Engineering',
        'date_posted': 'April 08, 2021'
    },
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Success! Account created for {form.username.data}.')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)