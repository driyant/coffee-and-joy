from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:driyant@localhost/db_coffeeshop"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category_name = db.Column(db.String(50), nullable=False)
  menu = db.relationship('Menu', backref='id_category', lazy='joined')
  
class Menu(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  menu_name = db.Column(db.String(100), nullable=False)
  menu_description = db.Column(db.String(200), nullable=False)
  menu_photo = db.Column(db.String(500), nullable=False)
  id_category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Subscriber(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subscriber_firstname = db.Column(db.String(50), nullable=False)
  subscriber_lastname = db.Column(db.String(50), nullable=False)
  subscriber_email = db.Column(db.String(50), nullable=False)

  def __init__(self, subscriber_firstname, subscriber_lastname, subscriber_email):
    self.subscriber_firstname = subscriber_lastname
    self.subscriber_lastname = subscriber_lastname
    self.subscriber_email = subscriber_email

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(50), nullable=False)
  event_promo_info = db.Column(db.String(255), nullable=False)
  event_date_info = db.Column(db.String(200), nullable=False)
  event_date_end = db.Column(db.DateTime, nullable=False)

  def __init__(self, event_name, event_info, event_date, event_status):
    self.event_name = event_name
    self.event_info = event_info
    self.event_date = event_date
    self.event_status = event_status

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
  return render_template("admin_dashboard/category.html")

@app.route("/admin_dashboard/category/add", methods=["GET", "POST"])
def category_add():
  if request.method == "POST":
    # Get form category value
    category = request.form["category"]
    print(category)
    return redirect(url_for('category'))
  else:
    return render_template("admin_dashboard/category_add.html")

@app.route("/admin_dashboard/event")
def event():
  #Fetch all data in event list
  return render_template('admin_dashboard/event.html')

if __name__ == "__main__":
  app.run(debug=True)