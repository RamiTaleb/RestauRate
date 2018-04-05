from settings import app, db

class Rater(db.Model):
	username = db.Column(db.String, primary_key=True, unique=True)
	email = db.Column(db.String, unique=True)
	name = db.Column(db.String)
	join_date = db.Column(db.Date)
	reputation = db.Column(db.Integer, db.CheckConstraint('reputation<=5'), db.CheckConstraint('reputation>=1'), default=1, nullable=False)
	raterType = db.Column(db.String)

	def __init__(self, username, email, name, join_date, reputation, raterType):
		self.username = username
		self.email = email
		self.name = name
		self.join_date = join_date
		self.reputation = reputation
		self.raterType = raterType

	def __repr__(self):
		return '<Rater %r>' % self.username


class Rating(db.Model):
	id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), unique=True, primary_key=True)
	user = db.Column(db.String, db.ForeignKey('rater.username'), nullable=False)
	restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantId'), nullable=False)
	date = db.Column(db.DateTime)
	price = db.Column(db.Integer, db.CheckConstraint('price<=5'), db.CheckConstraint('price>=1'))
	food = db.Column(db.Integer, db.CheckConstraint('food<=5'), db.CheckConstraint('food>=1'))
	mood = db.Column(db.Integer, db.CheckConstraint('mood<=5'), db.CheckConstraint('mood>=1'))
	staff = db.Column(db.Integer, db.CheckConstraint('staff<=5'), db.CheckConstraint('staff>=1'))
	comments = db.Column(db.Text)

	def __init__(self, user, date, price, food, mood, staff, comments, restaurant):
		self.user = user
		self.date = date
		self.price = price
		self.food = food
		self.mood = mood
		self.staff = staff
		self.comments = comments
		self.restaurant = restaurant

	def __repr__(self):
		return '<Rating %r, %r>' % (self.user, self.date)


class Restaurant(db.Model):
	restaurantId = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String)
	restaurantType = db.Column(db.String)
	url = db.Column(db.String)

	def __init__(self, name, restaurantType, url):
		self.name = name
		self.restaurantType = restaurantType
		self.url = url

	def __repr__(self):
		return '<Restaurant %r>' % self.restaurantId 


class Location(db.Model):
	locationId = db.Column(db.Integer, primary_key=True, unique=True)
	manager_name = db.Column(db.String)
	phone_number = db.Column(db.String)
	street_address = db.Column(db.String)
	hour_open = db.Column(db.Time)
	hour_close = db.Column(db.Time)
	restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantId'), nullable=False)

	def __init__(self, manager_name, phone_number, street_address, hour_open, hour_close, restaurant):
		self.manager_name = manager_name
		self.phone_number = phone_number
		self.street_address = street_address
		self.hour_open = hour_open
		self.hour_close = hour_close
		self.restaurant = restaurant

	def __repr__(self):
		return '<Location %r, Restaurant %r>' % (self.locationId, self.restaurant)


class MenuItem(db.Model):
	itemId = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), unique=True)
	name = db.Column(db.String, primary_key=True)
	itemType = db.Column(db.String)
	category = db.Column(db.String)
	description = db.Column(db.Text)
	price = db.Column(db.Integer)
	restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantId'), nullable=False, primary_key=True)

	def __init__(self, name, itemType, category, description, price, restaurant):
		self.name = name
		self.itemType = itemType
		self.category = category
		self.description = description
		self.price = price
		self.restaurant = restaurant

	def __repr__(self):
		return '<MenuItem %r, Restaurant %r>' % (self.name, self.restaurant)


class RatingItem(db.Model):
	user = db.Column(db.String, db.ForeignKey('rater.username'), nullable=False, primary_key=True)
	item = db.Column(db.Integer, db.ForeignKey('menu_item.itemId'), nullable=False, primary_key=True)
	date = db.Column(db.DateTime)
	rating = db.Column(db.Integer, db.CheckConstraint('rating<=5'), db.CheckConstraint('rating>=1'))
	comment = db.Column(db.String)

	def __init__(self, user, item, date, rating, comment):
		self.user = user
		self.item = item
		self.date = date
		self.rating = rating
		self.comment = comment

	def __repr__(self):
		return '<RatingItem: User %r, Date %r>' % (self.user, self.date)

#db.create_all()
