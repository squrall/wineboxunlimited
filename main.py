import sqlite3
import json
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from flask import Flask, render_template, request, redirect

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():

    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM wine_reviews').fetchall()
    conn.close()

    customer_preference = "Merlot"

    return render_template('index.html', reviews=reviews, customer_preference=customer_preference)

@app.route('/wineinput', methods= ['POST'])
def wine_input():

    variety = request.form['variety'].strip()
    region = request.form['region'].strip()
    min_rating = request.form['rating'].strip()
    if(min_rating == ''):
        min_rating = 0

    min_price = request.form['min_price'].strip()
    if min_price == '':
        min_price = 0 ## Arbitrary large number

    max_price = request.form['max_price'].strip()
    if max_price =='':
        max_price = 99999
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM wine_reviews WHERE variety LIKE ? AND state LIKE ? AND price BETWEEN ? AND ? AND ? < points',('%'+ variety +'%','%'+ region +'%', min_price, max_price, min_rating)).fetchall()
    conn.close()

    customer_preference = variety

    graphJSON = create_graph(reviews)

    return render_template('index.html', reviews=reviews, customer_preference=customer_preference, graphJSON=graphJSON)

def create_graph():


    N = 10
    x = np.linspace(0,10,N)
    y = 5
    df = pd.DataFrame({'x':x, 'y':y}) # Sample Dataframe

    graph = [go.Bar(x=df['x'],y=df['y'])]

    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
