import dataset
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#configuration
# DEBUG = True
# SECRET_KEY = 'development key'

app = Flask(__name__)
app.secret_key = 'hello'
# app.config.from_object((__name__))

db = dataset.connect('sqlite:///db.sqlite')
uname = 'Me, myself, and I'
pword = 'Robo appocolypse'

@app.route('/new')
def new():
	print('inside new')
	return render_template('new.html.jinja2')

@app.route('/post', methods=['POST'])
def post():
	username = request.form['username']
	message = request.form['message']
	db['posts'].insert(dict(username=username, message=message))
	return redirect('/posts')

@app.route('/posts')
def posts():
	return render_template('base.html.jinja2', content=list(db['posts']))

@app.route('/', methods=['GET', 'POST'])
def login():
	error =  None
	if request.method == 'POST':
		if request.form['username'] != uname:
			error = 'Invalid username'
		elif request.form['password'] != pword:
			error = 'Invalid password'
		else:
			print(session)
			session['logged_in'] = True
			print('before flash')
			flash('You were logged in')
			print('See me')
			return redirect('/new')
	return render_template('login.html.jinja2', error=error)

if __name__ == "__main__":
	app.run()
