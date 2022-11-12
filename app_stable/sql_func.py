import sqlite3   #enable control of an sqlite database
import os

# os.system('rm -rf discobandit.db') # this is to delete the dataframe file as to not encounter any errors during testing

# opens a connection with sql3 
def open_connection():
    try:
        db = sqlite3.connect('blog_database') #open if file exists, otherwise create
        c = db.cursor() # creates cursor object to pass commands to the database
        return {"db_obj":db, "cursor_obj":c}
    except Exception as e:
        print(f"an error just happened in sql_func.py, it is called {e}")
        return e
    

    

# creates table if and only it doesn't exist yet
def create_table():
    open_connection()
    
    c.execute(f'''create table if not exists {table_name}('{keys[0]}' text, {keys[1]} int, {keys[2]} text);''') # creates the table
    

# adds an entry to a specific table that already exists
def add_entry():
    return "hi"

# read an entry from a specific table that already exists
def read_entry():
    return "boo"

# edits an entry (only one) in a specific table
def edit_entry():
    return "hawoo"
    
    





def populate_table(file_name,table_name,elements,keys):

    db = sqlite3.connect(file_name) #open if file exists, otherwise create
    c = db.cursor() # creates cursor object to pass commands to the database

    c.execute(f'''create table if not exists {table_name}('{keys[0]}' text, {keys[1]} int, {keys[2]} text);''') # creates the table
    for row in elements:

        # iterate through the elements and add them to the table ( row by row )
        c.execute(f'''insert into {table_name} values('{row[keys[0]]}',{row[keys[1]]},'{row[keys[2]]}');''') 

    c.execute(f'''select * from {table_name}''') # for some reason need this execute statment to get fetchall
    return_msg = c.fetchall() # returns a list of tuples that are rows

    db.commit() #save changes
    db.close()  #close database
        
    return (return_msg)










