# app.py
#certain things are capitalized for me to easier find modifiers as we were taught in class
#also has other uses I didn't really use in class.

from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

#define the path to the SQLite database
db_path = "mydb.db"

#function to create the table if it doesn't exist
#deviated from basic structure with the assumption large amounts of data won't be stored but could use a file to make it bigger.

def create_table():
    with sqlite3.connect(db_path) as con:
        con.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                description TEXT,
                price REAL,
                code TEXT
            )
        ''')
        #this keeps it in the file
        con.commit()

#home Page
@app.route('/', methods=["GET", 'POST'])
def home():
    return render_template('index.html')

#enter Product Data
#post is input get is something idk. i got help on this one. does not impact whether its there or not
@app.route('/enter_product', methods=['GET', 'POST'])
def enter_product():
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        price = float(request.form['price'])
        code = request.form['code']

        with sqlite3.connect(db_path) as con:
            con.execute('INSERT INTO products (category, description, price, code) VALUES (?, ?, ?, ?)',
                        (category, description, price, code))
            con.commit()
        #sends back
        return redirect('/')
    return render_template('enter_product.html')

#retrieve Product Data
#GET and POST specify how the data is sent and saves it or displays it 
#generally uses POST but get could be used eventually.
#can't figure out a home button
@app.route('/retrieve_product', methods=['GET', 'POST'])
def retrieve_product():
    if request.method == 'POST':
        category = request.form.get('category', None)

        #mentioning again, stored in python :) i like it but the company would not
        with sqlite3.connect(db_path) as con:
            if category:
                result = con.execute('SELECT * FROM products WHERE category = ?', (category,))
            else:
                result = con.execute('SELECT * FROM products')

            #select's all the products from that category entered
            products = result.fetchall()

        return render_template('retrieve_product.html', products=products)

    return render_template('retrieve_product.html')

#checks if being run directly
#makes the table
#i like debug mode :)
if __name__ == '__main__':
    create_table()
    app.run(debug=True)
