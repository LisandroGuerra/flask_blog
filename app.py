from datetime import datetime
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm


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
        'author': 'Lisandro S Pires',
        'email': 'lis@blog.com',
        'title': 'Post 1',
        'content': 'Python Programing',
        'date_posted': 'April 08, 2022'
    },
    {
        'author': 'Maria Moreira',
        'email': 'cida@blog.com',
        'title': 'Post 2',
        'content': 'Human Resources',
        'date_posted': 'February 05, 2022'
    },
    {
        'author': 'Lisandra S Pires',
        'email': 'lica@blog.com',
        'title': 'Post 3',
        'content': 'Graphos Theory',
        'date_posted': 'September 30, 2022'
    },
    {
        'author': 'Anita G S Pires',
        'email': 'nita@blog.com',
        'title': 'Post 4',
        'content': 'Jewelery tips',
        'date_posted': 'November 14, 2022'
    },
    {
        'author': 'Lisandro Guerra',
        'email': 'lix@blog.com',
        'title': 'Post 5',
        'content': 'Software Engineering',
        'date_posted': 'April 08, 2021'
    },
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Success! Account created for {form.username.data}.')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'{form.username.data} Login Success!')
            return redirect(url_for('home'))
        else:
            flash('Login fail. Please check your password and username')
    return render_template('login.html', title='Login', form=form)


def new_user_from_dict(user_data):
    username = user_data['author']
    email = user_data['email']
    password = email.split('@')[0]
    return User(username=username, email=email, password=password)


def new_post_from_dict(post_data):
    title = post_data['title']
    content = post_data['content']
    user_id = int(title.split()[1])
    return Post(title=title, content=content, user_id=user_id)
    

# # Data Base operations
# with app.app_context():
#     db.create_all()
#     db.drop_all()
#     db.create_all()

#     for post in posts:
#         new_user = new_user_from_dict(post)
#         db.session.add(new_user)
#     db.session.commit()

#     for post in posts:
#         new_post = new_post_from_dict(post)
#         db.session.add(new_post)
#     db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)