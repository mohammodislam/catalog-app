import functools
import string
import random
from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import db_session
from models import Users

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		old_user = None
		try: 
			old_user = Users.query.filter(Users.username == username).first()
		except:
			pass
		# Validation
		error = None
		if not username:
			error = 'Username is required!'
		elif not password:
			error = 'Password is required!'
		elif old_user is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			u = Users(username=username, password=generate_password_hash(password), api_key= randomString(10))
			db_session.add(u)
			db_session.commit()
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = Users.query.filter(Users.username == username).first()
		# Validation
		error = None
		if username is None:
			error = 'Username is required!'
		elif password is None:
			error = 'Password is required!'
		elif user is None:
			error = 'Incorrect Username!'
		elif not check_password_hash(user.password, password):
			error = 'Incorrect password!'

		if error is None:
			session.clear()
			session['user_id'] = user.id
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))



@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = Users.query.filter(Users.id == user_id).one()

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view

def randomString(stringLength=10):
	"""Generate a random string of fixed length """
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))
