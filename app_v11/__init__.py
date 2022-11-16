from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import redirect, request, session, url_for
from sql_func import *
from datetime import datetime
import random

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

@app.route('/explore', methods=['GET', 'POST'])
def explore():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']

    all_ids = read_allcol("blogs", "blog_id", "author", "title")
    blogs=[0, 0, 0, 0, 0]
    if len(all_ids) >= 5:
        for i in range(5):
            blogs[i] = list(random.choice(all_ids))
            print(blogs[i][0])
            blogs[i][0] = blogs[i][0]

    if request.method == 'POST':
        print("hi")
        print(request.form['blog_id'])
        session['viewing_blog_id'] = request.form['blog_id']
        return redirect(url_for('blog'))

    return render_template('explore.html',\
        blog1=blogs[0][0], blog2=blogs[1][0], blog3=blogs[2][0], blog4=blogs[3][0], blog5=blogs[4][0],\
        blog1_title=blogs[0][2], blog2_title=blogs[1][2], blog3_title=blogs[2][2], blog4_title=blogs[3][2],blog5_title=blogs[4][2]\
    )

@app.route('/home', methods = ["GET","POST"])
def home():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']

    my_blogs = []

    all_ids = read_allcol("blogs", "blog_id", "author", "title")
    for id in all_ids:
        if id[1] == curr_usr:
            my_blogs.append(id)

    # blogs = [0,0,0,0,0]
    # if len(my_blogs) == 0:
    #     return render_template('home.html',text="no blogs published")
    # if len(my_blogs) >= 5:
    #     for i in range(5):
    #         blogs[i] = list(random.choice(my_blogs))
    #         print(blogs[i][0])
    #         blogs[i][0] = blogs[i][0]

    html_input = '''<!DOCTYPE html> <html> <head> <link rel="stylesheet" href="{{ url_for('static',filename='styles/style.css') }}"> </head> <style> { border: solid black; } #blog_button { color: transparent; font-size: 0%; color: none; } #blog_label { margin-left: 5%; font-size: large; } body { background-color: ivory; font-family: Helvetica, Arial, sans-serif; } h2 { font-size: 40px; color: lightsalmon; } h1 { font-size: 60px; color: coral; text-decoration: underline; text-decoration-color: black; } h3 { font-size: 30px; color: tomato; } a { color: palevioletred; text-decoration: none; } a.current-page { background-color: lightcyan; } a.moreinfo { float: right; } a:hover { color: hotpink; font-style: italic; text-decoration: underline; background-color: lightgoldenrodyellow; } nav { list-style-type: none; overflow: hidden; background-color: khaki; } nav a { border: groove lightsalmon; float: left; display: block; text-align: center; padding: 16px; } div.body { display: flex; } div.text { display: block; margin: 1%; } div.stat-text { max-width: 55%; display: block; margin-left: 3%; margin-top: 5%; float: right; } div.large-stat-text { max-width: 95%; display: block; margin: auto; } div.right-img { margin: auto; max-width: 50% } div.left-img { max-width: 70%; } div.next-page { margin: 5%; text-align: center; } div.stat-left { max-width: 50%; padding: 1%; float: left; } div.large-stat-left { display: block; padding: 1%; max-width: 100% } div.large-stat-left3 { display: block; padding: 1%; max-width: 120% } img.left { width: 100%; height: auto; } img { border: groove lightsalmon; } img.stat-left { max-width: 100%; padding: 12%; height: 70%; width: auto; } img.large-stat-left { width: 75%; display: block; margin-left: auto; margin-right: auto; } img.large-stat-left3 { width: 90%; display: block; margin-left: auto; margin-right: auto; } </style> <body> <form action="/"> <input type="submit" value="Back"/> </form> <div class="tabs"> <a href="home">Home</a> <a href="explore">Explore</a> <a href="create">Create</a> <!-- <a class="current-page" href="goodpets.html">Why They're Good Pets</a> <a href="moreinfo.html">Continue Learning about Frogs</a> --> </div> <h1>Home!</h1> <div> <form method="POST">'''
    html_end = '''</form></div></body></html>'''

    html_temp = '''
<br>
    <label id="blog_label">
    {}
        <button type="submit" name="blog_id" id="blog_button" placeholder= {} value={}></button><br/>
    </label>
<br>'''

    for blog in my_blogs:
        blog_title = blog[2]
        blog_id = str(blog[0])
        html_input += (html_temp.format(blog_title,blog_title,blog_id))
    
    # print(html_input+html_end)
    '''<br>
            <label id="blog_label">
            {blog1_title}
                <button type="submit" name="blog_id" id="blog_button" placeholder={{blog1_title}} value={{blog1}}></button><br/>
            </label>
        <br>'''

    if request.method == 'POST':
        print("hi")
        print(request.form['blog_id'])
        session['viewing_blog_id'] = request.form['blog_id']
        return redirect(url_for('blog'))

    print(html_input+html_end)



    # return render_template('home.html',\
    #     blog1=blogs[0][0], blog2=blogs[1][0], blog3=blogs[2][0], blog4=blogs[3][0], blog5=blogs[4][0],\
    #     blog1_title=blogs[0][2], blog2_title=blogs[1][2], blog3_title=blogs[2][2], blog4_title=blogs[3][2],blog5_title=blogs[4][2]\
    # )
    # return render_template('home.html',all_blogs=html_input)
    return (html_input+html_end)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']
    all_ids = read_allcol("blogs", "blog_id", "author", "content_body", "title")
    title="Doesn't exist"
    body="RIP"
    usr="John Smith"
    for blog_info in all_ids:
        blog_info = list(blog_info)
        # print(session['viewing_blog_id'])
        # print(blog_info[0]))
        if str(blog_info[0]) == session['viewing_blog_id']:
            print("made it")
            title=blog_info[3]
            body=blog_info[2]
            usr=blog_info[1]
            break
    return render_template('blog.html', title=title, body=body, usr=usr)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session and 'password' not in session:
        return redirect(url_for('login'))
    curr_usr = session['username']

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body']
        blurb = request.form['blog_blurb']
        today = datetime.now()
        today = today.strftime("%d/%m/%Y %H:%M:%S")
        blog_id = random.randrange(1000000000)
        while entry_exists("blogs", ("blog_id", blog_id)):
            blog_id = random.randrange(1000000000)
        add_entry("blogs", (blog_id, curr_usr, title, today, blurb, body))
    return render_template('create.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session and 'password' not in session and request.method == 'POST': # and 'username' in session and 'password' in session:
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    if 'username' in session:
        # print(session)
        # print(entry_exists("usernames", ("username", session['username'])))
        if entry_exists("usernames", ("username", session['username'])):
            # print (read_entry("usernames", ("username", session['username']),"password"))
            if read_entry("usernames", ("username", session['username']),"password")[0] == session['password']:
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
            if not entry_exists("usernames", ("username",new_usr)):
                add_entry("usernames", (new_usr, new_pass))
            else:
                msg = "Username already taken"
                return render_template("add_account.html", msg=msg)
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
    delete_entry("usernames", ("username", session['username'])) 
    session.pop('username', None)
    session.pop('password', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
