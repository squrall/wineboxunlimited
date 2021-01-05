/*DROP TABLE IF EXISTS wine_reviews;*/

CREATE TABLE wine_reviews
 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    country TEXT,
    description TEXT,
    designation TEXT,
    points INT,
    price INT,
    state TEXT,
    region_1 TEXT,
    region_2 TEXT,
    taster_name TEXT,
    title TEXT,
    variety TEXT,
    winery TEXT
);