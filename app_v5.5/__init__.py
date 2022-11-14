from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import redirect, request, session, url_for
from sql_func import *

app = Flask(__name__)    #create Flask object

app.secret_key = 'skey'
usernames=['yee', 'ah']
passwords = ['goofy', 'ah']


@app.route('/')
def index():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('index.html', username=curr_usr)

@app.route('/home')
def home():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('home.html', username=curr_usr)

@app.route('/explore')
def explore():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('explore.html', username=curr_usr)

@app.route('/create')
def create():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    return render_template('create.html', username=curr_usr)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session and 'password' not in session and request.method == 'POST': # and 'username' in session and 'password' in session:
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    if 'username' in session:
        if session['username'] in usernames:
            if passwords[usernames.index(session['username'])] == session['password']:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                msg = 'Wrong password'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Wrong username'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        session['nusername'] = request.form['nusername']
        session['npassword'] = request.form['npassword']
        session['vnusername'] = request.form['vnusername']
        session['vnpassword'] = request.form['vnpassword']

    if 'nusername' in session and 'npassword' in session:
        if session['nusername'] ==  session['vnusername'] and session['npassword'] == session['vnpassword']:
            new_usr = session['nusername']
            new_pass = session['npassword']
            add_entry("usernames", (new_usr, new_pass))
            session.pop('nusername', None)
            session.pop('npassword', None)
            session.pop('vnusername', None)
            session.pop('vnpassword', None)
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('login'))

        elif session['nusername'] != session['vnusername']:
            if session['npassword'] != session['vnpassword']:
                msg = "Usernames and passwords don't match"
                return render_template('add_account.html', msg=msg)
            else:
                msg = "Usernames don't match"
                return render_template('add_account.html', msg=msg)
        else:
            msg = "Passwords don't match"
            return render_template('add_account.html', msg=msg)
    return render_template('add_account.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/delete_account')
def delete_account():
    # remove the username from the session if it's there
    usr_index = delete_entry("usernames", session['username']) 
    usernames.pop(usr_index)
    passwords.pop(usr_index)
    session.pop('username', None)
    session.pop('password', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
