from flask import Flask, render_template, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SECRET_KEY"] = "1f157c192086567f577cc2fe83a45091"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app=app)

from models import User, Post

# This is list of dictionary of posts
posts = [
    {
        'title': 'Blog Post 1',
        'author': 'Mr. Schafer',
        'date': '12-04-2019',
        'content': 'This is First Blog Post.'
    },

    {
        'title': 'Blog Post 2',
        'author': 'Mr. Harry',
        'date': '01-05-2019',
        'content': 'This is Second Blog Post.'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", posts=posts, title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect('/home')
    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You have successfully loged in", 'success')
            return redirect('/home')
        else:
            flash("Login Unsuccessful. Please, check username and password!", 'danger')
    return render_template("login.html", title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
