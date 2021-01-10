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

def create_graph(reviews):
    y = 0
    wine_location = []
    wine_count = []

    for review in reviews:

        count = 0

        if review[7] not in wine_location:
            wine_location.append(review[7])
            wine_count.append(0)

        while count < len(wine_location):
            if review[7] == wine_location[count]:
                wine_count[count] += 1

            count += 1
        y += 1

    count = 0
    while count < len(wine_location):
        if len(wine_location) > 20:
            if wine_count[count] <= 20:
                del wine_count[count]
                del wine_location[count]

            else: count +=1
        else: break

    print(f"{y} {wine_location} {wine_count}")


    graphs = dict(
                data=[go.Bar(
                        x=wine_location,
                        y=wine_count,
                    )
                ],
                layout=dict(
                    title="Wine Count via Region",
                    yaxis=dict(title="Wine Count")
                    #xaxis=dict(title="Region")
                )
            )


    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
