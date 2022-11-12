from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import redirect, request, session, url_for

app = Flask(__name__)    #create Flask object

app.secret_key = 'hi'
usernames=['yee', 'ah']
passwords = ['goofy', 'ah']

@app.route('/')
def index():
    if 'username' in session and 'password' in session:
        curr_usr = session['username']
        print(curr_usr)
        return render_template('index.html', username=curr_usr)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = (request.form['username'])
        session['password'] = (request.form['password'])
        
        if session['username'] in usernames:
            if passwords[usernames.index(session['username'])] == session['password']:
                return redirect(url_for('index'))
            else:
                msg = 'Wrong password'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Wrong username'
            return render_template('login.html', msg=msg)
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()