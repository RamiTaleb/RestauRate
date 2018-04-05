from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbFiller import populateRestaurantTable, populateMenuTable, populateRaterTable, populateRatingTable, populateMenuItemRatingTable
from settings import app, db

#populateRaterTable(db)

#populateRestaurantTable(db)

#populateMenuTable(db)

#populateRatingTable(db)

#populateMenuItemRatingTable(db)

@app.route('/')
def index():
	return "<h1 style='color: red'>Hello World<h1>"


if __name__ == '__main__':
	app.run()

