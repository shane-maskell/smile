from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DB_NAME = "C:/Users/18406/OneDrive - Wellington College/13DTS/Smile/smile.db"

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "AHhguwhduYAQjwnIdhwnUdne"

def create_connection(db_file):

    """
    Create a connection with the database
    paramater: name of the database file
    returns: a connection to the file
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None

def is_logged_in():
    """
    A function to return whether a user is logged in or not.
    """
    if session.get("email") is None:
        print("Not logged in")
        return False
    else:
        print("Logged in")
        return True
@app.route('/')
def render_homepage():
    return render_template('home.html', logged_in=is_logged_in())


@app.route('/menu')
def render_menu_page():
    con = create_connection(DB_NAME)

    query = "SELECT name, description, volume, price, image FROM products"
    cur = con.cursor()      # Creates a cursor to write the query
    cur.execute(query)      # Runs the query
    product_list = cur.fetchall()
    con.close()

    return render_template('menu.html', products=product_list, logged_in=is_logged_in())


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html', logged_in=is_logged_in())

@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password)
        con = create_connection(DB_NAME)
        query = "SELECT id, fname FROM customer WHERE email=? AND password=?"
        cur = con.cursor()
        cur.execute(query, (email, hashed_password))
        user_data = cur.fetchall()
        con.close()

        if user_data:
            user_id = user_data[0][0]
            first_name = user_data[0][1]
            db_password = user_data[0][2]
        else:
            return redirect("login?error=Email+or+password+is+incorrect")

        if not bcrypt.check_password_hash(db_password, password):
        #Set up a session for this login.
        session['email'] = email
        session['username'] = user_id
        session['fname'] = first_name
        session['cart'] = []
        return redirect('/')

    return render_template('login.html', logged_in=is_logged_in())

@app.route('/logout')
def render_logout_page():
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect("/?message=See+you+next+time")

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

        hashed_password = bcrypt.generate_password_hash(password)
        con = create_connection(DB_NAME)

        query = "INSERT INTO customer (name, lname, email, password) VALUES (?, ?, ?, ?)"

        cur = con.cursor()
        cur.execute(query, (name,lname, email, hashed_password))
        con.commit()
        con.close()
        return redirect('/login')

    error = request.args.get('error')
    if error == None:
        error = ""
    return render_template('signup.html', error=error, logged_in=is_logged_in())


app.run(host='0.0.0.0', debug=True)
