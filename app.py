from flask import Flask, render_template, request, redirect
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
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')

        con = create_connection(DB_NAME)
        query = "SELECT id, fname FROM customer WHERE email=? AND password=?"
        cur = con.cursor()
        cur.execute(query, (email, password))
        user_data = cur.fetchall()
        con.close()

        try:
            user_id = user_data[0][0]
            first_name = user_data[0][1]
        except indexError:
            return redirect("login?error=Email+or+password+is+incorrect")
        print(user_id, first_name)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if request.method == 'POST':
        print(request.form)
        name = request.form.get('fname').title().strip()
        lname = request.form.get('lname').title().strip()
        email = request.form.get('email').title().strip()
        password = request.form.get('password')
        password2 = request.form.get('password2')


        if password != password2:
            return redirect('/signup?error=Passwords+do+not+match')

        if len(password) < 8:
            return redirect('/signup?error=Passwords+must+be+at+least+8+characters')

        con = create_connection(DB_NAME)

        query = "INSERT INTO customer (name, lname, email, password) VALUES (?, ?, ?, ?)"

        cur = con.cursor()
        cur.execute(query, (name,lname, email, password))
        con.commit()
        con.close()
        return redirect('/login')

    error = request.args.get('error')
    if error == None:
        error = ""
    return render_template('signup.html', error=error)


app.run(host='0.0.0.0', debug=True)
