from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DB_NAME = "C:/Users/18406/OneDrive - Wellington College/13DTS/Smile/smile.db"

app = Flask(__name__)

def create_connection(db_file):
    ###
    # Create a connection with the database
    # paramater: name of the database file
    # returns: a connection to the file
    ###
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    con = create_connection(DB_NAME)

    query = "SELECT name, description, volume, price, image FROM products"
    cur = con.cursor()      # Creates a cursor to write the query
    cur.execute(query)      # Runs the query
    product_list = cur.fetchall()
    con.close()

    return render_template('menu.html', products=product_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    return render_template('signup.html')

app.run(host='0.0.0.0', debug=True)
