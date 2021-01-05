import sqlite3
import csv

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

with open('./static/winereview-utf8-excel-v1.0.csv', newline='', encoding='utf-8') as wine_csv:
    open_csv = csv.reader(wine_csv, delimiter=',')
    line_count = 1
    for row in open_csv:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            cursor.execute("INSERT INTO wine_reviews (country, description, designation, points, price, state, region_1, region_2, taster_name, title, variety, winery) VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?)",
                           (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[11], row[12], row[13],)
                           )
        print(f'Processed {line_count} lines.')

connection.commit()
connection.close()
