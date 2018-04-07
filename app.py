from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbFiller import *
from settings import app, db
from models import *
from flask import render_template, redirect, url_for
from sqlalchemy import text


#populateRaterTable(db)

#populateRestaurantTable(db)

#populateMenuTable(db)

#populateRatingTable(db)

#populateMenuItemRatingTable(db)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/query')
def query():
	sql = text('select * from menu_item')
	raters = db.engine.execute(sql)
	print ('SELECT * FROM Restaurant R, Location L WHERE R.name = $restaurantName AND R.\"restaurantId\" = L.restaurant;')
	return render_template('query.html', raters=raters)


if __name__ == '__main__':
	app.run()

