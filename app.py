from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:driyant@localhost/db_coffeeshop"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_coffeeshop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

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


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    # Get input value
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    data = Subscriber(firstname,lastname,email)
    db.session.add(data)
    db.session.commit()
    print("Success!", firstname, lastname, email)
    return render_template("index.html")
  else:
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin" and password == "admin123":
      return redirect(url_for("admin_dashboard"))
    else:
      print("Invalid username or password")
      return render_template("login.html")   
  else:
    return render_template("login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
  return render_template("admin_dashboard/admin.html")

@app.route("/admin_dashboard/subscriber")
def subscriber():
   # Fetch all data in subscriber list
  data_subscriber = Subscriber.query.all()
  print(data_subscriber)
  return render_template('admin_dashboard/subscriber.html', subscribers = data_subscriber)

@app.route("/admin_dashboard/category")
def category():
  # Fetch all category data
  categories = Category.query.all()
  return render_template("admin_dashboard/category.html", categories = categories)

@app.route("/admin_dashboard/category/add", methods=["GET", "POST"])
def category_add():
  if request.method == "POST":
    # Get form category value
    category = request.form["category"].lower()
    data = Category(category)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('category'))
  else:
    return render_template("admin_dashboard/category-add.html")

@app.route("/admin_dashboard/category/edit/<int:id>", methods=["GET","POST"])
def category_edit(id):
  category = Category.query.filter_by(id=id).first()
  if request.method == "POST":
    try:
      # Get input value
      category.category_name = request.form["category"].lower()
      db.session.commit()
      return redirect(url_for("category"))
    except:
      print("there is an issue")
      return redirect(url_for("category"))
  else:
    return render_template("admin_dashboard/category-edit.html", category=category)

@app.route("/admin_dashboard/category/delete/<id>", methods=["GET", "POST"])
def category_delete(id):
  try:
    data = Category.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("category"))
  except:
    print("There is an issue!")
    return redirect(url_for("category"))
  
@app.route("/admin_dashboard/menu", methods=["GET"])
def menu():
  menus = Menu.query.all()
  return render_template("admin_dashboard/menu.html", menus=menus)

@app.route("/admin_dashboard/menu/add", methods=["GET","POST"])
def menu_add():
  # Get category menu
  categories = Category.query.all()
  if request.method == "POST":
    # Get input value
    menu_name = request.form["menu_name"].lower()
    menu_description = request.form["menu_description"].lower()
    # Select category
    menu_category = request.form["menu_category"].lower()
    selected = Category.query.filter_by(category_name=menu_category).first()
    # Passing data into Menu class
    data = Menu(menu_name, menu_description, selected.id)
    # Session add db
    db.session.add(data)
    # Session commit db
    db.session.commit()
    return redirect(url_for('menu'))
  return render_template("admin_dashboard/menu-add.html", categories=categories)

@app.route("/admin_dashboard/menu/edit/<int:id>", methods=["GET","POST"])
def menu_edit(id):
  menu = Menu.query.filter_by(id=id).first()
  categories = Category.query.all()
  if request.method == "POST":
    try:
      menu.menu_name = request.form["menu_name"]
      menu.menu_description = request.form["menu_description"]
      
      db.session.commit()
      return redirect(url_for("menu"))
    except:
      print("There is something wrong!")
      return redirect(url_for("menu"))
  else:
    return render_template("admin_dashboard/menu-edit.html", menu=menu, categories=categories)

@app.route("/admin_dashboard/event")
def event():
  #Fetch all data in event list
  return render_template('admin_dashboard/event.html')

@app.route("/admin_dashboard/event/add")
def event_add():
  return render_template("admin_dashboard/event-add.html")

if __name__ == "__main__":
  app.run(debug=True)