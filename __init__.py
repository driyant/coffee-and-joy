db = SQLAlchemy(app)

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category_name = db.Column(db.String(50), nullable=False)
  menus = db.relationship('Menu', backref="category", lazy="joined")

  def __init__(self, category_name):
    self.category_name = category_name

class Menu(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  menu_name = db.Column(db.String(100))
  menu_description = db.Column(db.String(200))
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

  def __init__(self, menu_name, menu_description, category_id):
    self.menu_name = menu_name
    self.menu_description = menu_description
    self.category_id = category_id

    def __str__(self):
        return f"<Menu {self.name}>"

class Subscriber(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subscriber_firstname = db.Column(db.String(50), nullable=False)
  subscriber_lastname = db.Column(db.String(50), nullable=False)
  subscriber_email = db.Column(db.String(50), nullable=False)

  def __init__(self, subscriber_firstname, subscriber_lastname, subscriber_email):
    self.subscriber_firstname = subscriber_firstname
    self.subscriber_lastname = subscriber_lastname
    self.subscriber_email = subscriber_email

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(50), nullable=False)
  event_promo_info = db.Column(db.String(255), nullable=False)
  event_date = db.Column(db.DateTime, nullable=False)
  event_time = db.Column(db.String(100), nullable=False)
  event_place = db.Column(db.String(100), nullable=False)
  event_status = db.Column(db.String(20), nullable=False, default='upcoming')

  def __init__(self, event_name, event_promo_info, event_date, event_time, event_place, event_status):
    self.event_name = event_name
    self.event_promo_info = event_promo_info
    self.event_date = event_date
    self.event_time = event_time
    self.event_place = event_place
    self.event_status = event_status

db.create_all()
db.session.commit()
