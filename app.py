from flask import Flask, render_template

app = Flask(__name__)
DATABASE = smile.db

def create_connection(db_file):
    ###
    # Create a connection with the database
    # paramater: name of the database file
    # returns: a connection to the file
    ###
    try:
        connection = sqlite3.connect(db_file)
        return_connection
    except:
        print("Error")
        return None


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    con = create_connection(DATABASE)

    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor()      # Creates a cursor to write the query
    cur.execute(query)      # Runs the query
    product_list = cur.fetchall()
    con.close()

    return render_template('menu.html', products=product_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0', debug=True)
