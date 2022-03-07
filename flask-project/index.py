from distutils.log import debug
from email.policy import default
from pydoc import importfile
from wsgiref.util import request_uri
from aiohttp import request
from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from markupsafe import re
from sqlalchemy import PrimaryKeyConstraint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return "<Post %r>" % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return "<User %r>" % self.id


@app.route("/")
@app.route('/home')
def index():
    return render_template('index.html')


@app.route("/user_list")
def user_list():
    users = User.query.order_by(User.nickname.desc()).all()
    return render_template('user_list.html', users=users)


@app.route("/user_profile/<int:id>")
def user_profile(id):
    user = User.query.get(id)
    return render_template('post_view.html', user=user)


@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        nickname = request.form['nickname']
        name = request.form['name']

        user = User(nickname=nickname, name=name)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return "error"
    else:
        return render_template('create_profile.html')


@app.route("/new_post", methods=['POST', 'GET'])
def create_new_post():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        post = Post(title=title, intro=intro, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return "error"
    else:
        return render_template('new_post.html')


@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('posts.html', posts=posts)


@app.route('/posts/<int:id>')
def post_view(id):
    post = Post.query.get(id)
    return render_template('post_view.html', post=post)


@app.route('/posts/<int:id>/del')
def post_del(id):
    post = Post.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return "delete error"

@app.route("/posts/<int:id>/upt", methods=['POST', 'GET'])
def post_upt(id):
    post = Post.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "update error"
    else:
        return render_template('post_upt.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)