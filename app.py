#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn
from searchEngine import searchService
import json

app = Flask(__name__)
CORS(app)

#AUTHENTICATION:

app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1185910808162653',
        'secret': '6d443cdfad8286092c7b595e1927228c'
    },
    'twitter': {
        'id': 'N6OsA6bS7K5Jzi5F7OZrLRZjf',
        'secret': 'AnWXSpFKSNE4Lu1kb3mfrqEpuyKH3RiLt8DXqd163msiyu3frp'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

#END OF AUTHENTICATION

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/superJapi/api/v1.0/searchResult', methods=['GET', 'POST'])
def search():
	data1 = json.loads(request.data.decode())
	#print data1
	searchString = data1['userInput']
	returnSearch = searchService(str(searchString))
	#TODO: Maybe with the subprocess pakage, read in real time the pipe output to send an object to angularjs each time a specific string prints.
	return returnSearch

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)