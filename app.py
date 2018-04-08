from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbFiller import *
from settings import app, db
from models import *
from flask import render_template, redirect, url_for, request
from sqlalchemy import text
from models import Rater, Restaurant, Location, Rating, MenuItem, RatingItem


#populateRaterTable(db)

#populateRestaurantTable(db)

#populateMenuTable(db)

#populateRatingTable(db)

#populateMenuItemRatingTable(db)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/edit-menu-items')
def editMenuItems():
	sql = text('select "restaurantId", name from restaurant order by name')
	result = db.engine.execute(sql)
	return render_template('/edit-pages/edit-menu-items.html', result=result)


@app.route('/add-menu-item', methods=['GET', 'POST'])
def addMenuItem():
	item = MenuItem(name=request.form.get('name'), price=request.form.get('price'), restaurant=request.form.get('restaurant'), description=request.form.get('description'), itemType=request.form.get('type'), category=request.form.get('category'))
	db.session.add(item)
	db.session.commit()
	sql = text('select "restaurantId", name from restaurant order by name')
	result = db.engine.execute(sql)
	return render_template('/edit-pages/edit-menu-items.html', result=result)


@app.route('/edit-raters')
def editRaters():
	return render_template('/edit-pages/edit-raters.html')


@app.route('/add-rater', methods=['GET', 'POST'])
def addRater():
	rater = Rater(username=request.form.get('username'), email=request.form.get('email'), name=request.form.get('name'), join_date=str(datetime.date.today())[:10], reputation=1, raterType=request.form.get('raterType'))
	db.session.add(rater)
	db.session.commit()
	return render_template('/edit-pages/edit-raters.html')


@app.route('/edit-restaurants')
def editRestaurants():
	return render_template('/edit-pages/edit-restaurants.html')

@app.route('/query')
def query():
	sql1 = text('select name from restaurant order by name')
	sql2 = text('select name from restaurant order by name')
	sql3 = text('select DISTINCT("restaurantType") from restaurant order by "restaurantType"')
	sql4 = text('select name from restaurant order by name')
	result1 = db.engine.execute(sql1)
	result2 = db.engine.execute(sql2)
	result3 = db.engine.execute(sql3)
	result4 = db.engine.execute(sql4)
	return render_template('query.html', result1=result1, result2=result2, result3=result3, result4=result4)


@app.route('/a', methods=['GET', 'POST'])
def queryA():
	name = request.form.get('queryA')
	name1 = '\'' + name + '\''
	sql = '''SELECT * 
	 			FROM Restaurant R, Location L 
	 			WHERE R.name = '''+name1+''' AND R."restaurantId" = L.restaurant'''
	result = db.engine.execute(sql)
	return render_template('/query-pages/a.html', result=result)


@app.route('/b', methods=['GET', 'POST'])
def queryB():
	name = request.form.get('queryB')
	name1 = '\'' + name + '\''
	sql = '''SELECT MI.name as mname, MI.price, MI.description, MI.category 
				FROM menu_item MI 
				WHERE MI.restaurant = 
					(SELECT R."restaurantId" 
 					FROM Restaurant R 
 					WHERE R.name = '''+name1+''') 
 					ORDER BY category ASC'''
	result = db.engine.execute(sql)
	return render_template('/query-pages/b.html', result=result)


@app.route('/c', methods=['GET', 'POST'])
def queryC():
	name = request.form.getlist('queryC')
	names = []
	for i in range(len(name)):
		names.append('')
	for i in range(0, len(name)):
		names[i] = '\'' + name[i] + '\''
	names = str(names)
	names = names.replace('[','')
	names = names.replace(']','')
	names = names.replace('\"','')
	sql = '''SELECT DISTINCT(L.manager_name)
	 			FROM Location L, Restaurant R
	 			WHERE R."restaurantId" = L.restaurant AND R."restaurantType" IN ('''+names+''')'''
	result = db.engine.execute(sql)
	return render_template('/query-pages/c.html', result=result)


@app.route('/d', methods=['GET', 'POST'])
def queryD():
	name = request.form.get('queryD')
	name1 = '\'' + name + '\''
	sql = '''SELECT MI.name as mname, MI.price, L.manager_name, R.url, L.hour_open
				FROM Restaurant R, Location L, menu_item MI 
				WHERE MI.price >= 
				ALL(SELECT MI1.price 
					FROM menu_item MI1 
					WHERE MI1.restaurant = R."restaurantId") 
					AND R."restaurantId" = L.restaurant AND MI.restaurant = R."restaurantId" AND R.name = '''+name1+''''''
	result = db.engine.execute(sql)
	return render_template('/query-pages/d.html', result=result)


@app.route('/e')
def queryE():
	sql = text('''SELECT R."restaurantType", MI.category, AVG(MI.price) AS average_price 
				  FROM menu_item MI, Restaurant R 
				  WHERE MI.restaurant IN 
					   (SELECT R1."restaurantId" 
 						FROM Restaurant R1 
 						WHERE R1."restaurantType" = R."restaurantType") 
 				  AND MI.restaurant = R."restaurantId" 
 				  GROUP BY R."restaurantType", MI.category 
 				  ORDER BY R."restaurantType", MI.category''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/e.html', result=result)


@app.route('/f')
def queryF():
	sql = text('''SELECT U.username, R.name, AVG((R8.food + R8.mood + R8.staff + R8.price) / 4) as average_rating, COUNT(R8.*) as count 
					FROM Rating R8, Restaurant R, Rater U 
					WHERE R8.restaurant = R."restaurantId" AND R8.user = U.username 
					GROUP BY R.name, U.username 
					ORDER BY R.name, average_rating''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/f.html', result=result)


@app.route('/g')
def queryG():
	sql = text('''SELECT R.name, R."restaurantType", L.phone_number 
					FROM Restaurant R, Location L 
					WHERE NOT EXISTS
						(SELECT * 
 						FROM Rating R8 
 						WHERE date_part('year',R8.date) = 2015 AND date_part('month', R8.date) = 01 
 					AND R8.restaurant = R."restaurantId") AND R."restaurantId" = L.restaurant 
 					ORDER BY R.name''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/g.html', result=result)


@app.route('/h')
def queryH():
	sql = text('''SELECT R.name 
					FROM Restaurant R, Location L 
					WHERE R."restaurantId" IN 
						(SELECT R8.restaurant 
 						FROM Rating R8 
 						WHERE R8.staff < ANY(SELECT Rate.staff 
											FROM Rating Rate 
											WHERE Rate.user = 'Rami109')) 
											AND R."restaurantId" = L.restaurant''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/h.html', result=result)


@app.route('/i')
def queryI():
	sql = text('''SELECT R.name as rname, U.name as uname
					FROM Restaurant R, Rater U 
					WHERE R."restaurantId" IN 
						(SELECT R8.restaurant 
 						FROM Rating R8 
 						WHERE R8.restaurant IN 
 							(SELECT R1."restaurantId" 
  							FROM Restaurant R1 
  							WHERE R1."restaurantType" = 'Japanese') 
 						AND R8.food >= 
 							ALL(SELECT Rate.food 
	 						FROM Rating Rate 
							WHERE Rate.restaurant 
	 						IN (SELECT R2."restaurantId" 
								FROM Restaurant R2 
								WHERE R2."restaurantType" = 'Japanese')) 
 						AND R8.user = U.username)''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/i.html', result=result)


@app.route('/j')
def queryJ():
	sql = text('''SELECT restaurant.name, MAX(rating.food) AS food, MAX(rating.price) AS price, MAX(rating.mood) AS mood, MAX(rating.staff) AS staff
					FROM restaurant, rating
					WHERE restaurant."restaurantType" = 'Japanese'
					AND rating.restaurant = restaurant."restaurantId"
					GROUP BY restaurant.name, food, price, mood, staff
					HAVING food = (SELECT MAX(rating.food) AS food
									FROM restaurant, rating
									WHERE restaurant."restaurantType" = 'Japanese'
									AND rating.restaurant = restaurant."restaurantId"
					                )
					       AND price = (SELECT MAX(rating.price) AS price
									FROM restaurant, rating
									WHERE restaurant."restaurantType" = 'Japanese'
									AND rating.restaurant = restaurant."restaurantId"
					                )
					       AND staff = (SELECT MAX(rating.staff) AS staff
									FROM restaurant, rating
									WHERE restaurant."restaurantType" = 'Japanese'
									AND rating.restaurant = restaurant."restaurantId"
					                )
					       AND mood = (SELECT MAX(rating.mood) AS mood
									FROM restaurant, rating
									WHERE restaurant."restaurantType" = 'Japanese'
									AND rating.restaurant = restaurant."restaurantId"
					                )
					ORDER BY restaurant.name''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/j.html', result=result)


@app.route('/k')
def queryK():
	sql = text('''SELECT U.name as uname, U.join_date, U.reputation, R.name as rname, R8.date as rdate
					FROM Rater U, Restaurant R, Rating R8 
					WHERE U.username IN 
					(SELECT U1.username 
					 FROM Rater U1 
					 GROUP BY U1.username 
					 HAVING 
					 (SELECT AVG(Rate.mood + Rate.food) 
					  FROM Rating Rate 
					  WHERE Rate.user = U1.username) >= 
					 ALL(SELECT AVG(Rate1.mood + Rate1.food) 
						 FROM Rating Rate1, Rater U2 
						 WHERE Rate1.user = U2.username 
						 GROUP BY U2.username)) 
						 AND R8.user = U.username AND R8.restaurant = R."restaurantId"''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/k.html', result=result)


@app.route('/l')
def queryL():
	sql = text('''SELECT U.name as uname, U.join_date, U.reputation, R.name as rname, R8.date as rdate
					FROM Rater U, Restaurant R, Rating R8 
					WHERE U.username IN 
					(SELECT U1.username 
					 FROM Rater U1 
					 WHERE 
					 (SELECT AVG(mood) 
					  FROM Rating Rate 
					  WHERE Rate.user = U1.username) >= ALL(SELECT AVG(mood) 
											  FROM Rating Rate 
											  GROUP BY Rate.user) OR 
					(SELECT AVG(food) 
					FROM Rating Rate 
					WHERE Rate.user = U1.username) >= ALL(SELECT AVG(food) 
					FROM Rating Rate
					GROUP BY Rate.user))
					AND R8.user = U.username AND R8.restaurant = R."restaurantId"''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/l.html', result=result)


@app.route('/m')
def queryM():
	sql = text('''SELECT U.name, U.reputation, R8.comments 
					FROM Rating R8, Rater U 
					WHERE U.username IN 
					(SELECT U1.username 
					 FROM Rater U1 
					 WHERE 
					 (SELECT COUNT(*) 
					  FROM Rating Rate 
					  WHERE Rate.user = U1.username AND Rate.restaurant IN 
					  (SELECT R."restaurantId" 
					   FROM Restaurant R 
					   WHERE R.name = 'Big Daddy')) 
					 >=  All(SELECT COUNT(*) 
							FROM Rating Rate1 
							WHERE Rate1.restaurant IN 
							(SELECT R."restaurantId" 
							FROM Restaurant R 
							WHERE R.name = 'Big Daddy') 
							GROUP BY Rate1.user) 
					 AND R8.user = U.username AND R8.restaurant IN 
					 (SELECT R."restaurantId"
					  FROM Restaurant R 
					  WHERE R.name = 'Big Daddy'))''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/m.html', result=result)


@app.route('/n')
def queryN():
	sql = text('''SELECT U.name, U.email 
					FROM Rater U 
					WHERE U.username IN 
					(SELECT R8.user 
					 FROM Rating R8 
					 WHERE (R8.price + R8.food + R8.mood + R8.staff) 
					 < ANY(SELECT (Rate.price + Rate.mood + Rate.food + Rate.staff) 
						   FROM Rating Rate 
						   WHERE Rate.user IN 
						   (SELECT U1.username 
							FROM Rater U1 
							WHERE U1.name = 'John')))''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/n.html', result=result)


@app.route('/o')
def queryO():
	sql = text('''SELECT U.name as uname, U."raterType", U.email, R.name as rname, R8.food, R8.price, R8.mood, R8.staff, R8.comments 
					FROM Rater U, Rating R8, Restaurant R 
					WHERE U.username IN 
					(SELECT U1.username 
					 FROM Rater U1 
					 GROUP BY U1.username 
					 HAVING 
					 (SELECT max(stddev) 
					  FROM
					  (SELECT stddev(Rate.mood + Rate.staff + Rate.price +Rate.food) AS stddev 
					   FROM Rating Rate 
					   WHERE Rate.user = U1.username 
					   GROUP BY Rate.restaurant) AS W) 
					 >= ALL((SELECT max(stddev) 
							FROM 
							(SELECT stddev(Rate1.mood + Rate1.staff + Rate1.price +Rate1.food) 
							FROM Rating Rate1 
							GROUP BY Rate1.user, Rate1.restaurant) AS W))) 
							AND R8.user = U.username AND R8.restaurant = R."restaurantId" AND R."restaurantId" IN 
							(SELECT R2."restaurantId" 
							FROM Restaurant R2 
							GROUP BY R2."restaurantId" 
							HAVING 
							(SELECT max(stddev) 
							FROM
							(SELECT stddev(Rate2.mood + Rate2.staff + Rate2.price +Rate2.food) AS stddev 
							FROM Rating Rate2 
							WHERE Rate2.restaurant = R2."restaurantId" 
							GROUP BY Rate2.restaurant, Rate2.user) AS W) 
							>= ALL((SELECT max(stddev) 
									FROM 
									(SELECT stddev(Rate3.mood + Rate3.staff + Rate3.price +Rate3.food)
									FROM Rating Rate3 
									GROUP BY Rate3.user, Rate3.restaurant) AS W)))''')
	result = db.engine.execute(sql)
	return render_template('/query-pages/o.html', result=result)

if __name__ == '__main__':
	app.run()

