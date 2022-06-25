from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from forms import LoginForm 
from functools import wraps
from datetime import timedelta
from werkzeug.utils import secure_filename
import base64
from dateutil import parser
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import json
import datetime
import gunicorn

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_coffeeshop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

app.secret_key = '66700+!&##&+#ULHjek'
app.permanent_session_lifetime = timedelta(minutes=15)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()

csrf.init_app(app)
login_manager.init_app(app)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50))
  name = db.Column(db.String(70))
  password = db.Column(db.String(50))
  status = db.Column(db.String(30))
  
  def __init__(self, username, name, password, status):
    self.username = username
    self.name = name
    self.password = password
    self.status = status
    
  def __repr__(self):
    return f"<User {self.username} {self.name}>"

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category_name = db.Column(db.String(50), nullable=False)
  menus = db.relationship('Menu', backref="category", cascade="all,delete-orphan", lazy="joined")

  def __init__(self, category_name):
    self.category_name = category_name
  
  def __repr__(self):
    return f"<Category {self.category_name}>"

class Menu(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  menu_name = db.Column(db.String(100))
  menu_description = db.Column(db.String(200))
  menu_image = db.Column(db.Text, nullable=False)
  mimetype = db.Column(db.Text, nullable=False)
  menu_filename = db.Column(db.Text, nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

  def __init__(self, menu_name, menu_description, menu_image, menu_mimetype, menu_filename, category_id):
    self.menu_name = menu_name
    self.menu_description = menu_description
    self.menu_image = menu_image
    self.mimetype = menu_mimetype
    self.menu_filename = menu_filename
    self.category_id = category_id

  def __repr__(self):
    return f"<Menu {self.menu_name}>"

class Subscriber(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subscriber_firstname = db.Column(db.String(50), nullable=False)
  subscriber_lastname = db.Column(db.String(50), nullable=False)
  subscriber_email = db.Column(db.String(50), nullable=False)

  def __init__(self, subscriber_firstname, subscriber_lastname, subscriber_email):
    self.subscriber_firstname = subscriber_firstname
    self.subscriber_lastname = subscriber_lastname
    self.subscriber_email = subscriber_email
  
  def __repr__(self):
    return f"<Subscriber {self.subscriber_firstname}>"

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(50), nullable=False)
  event_promo_info = db.Column(db.String(255), nullable=False)
  event_date = db.Column(db.String(50), nullable=False)
  event_time = db.Column(db.String(100), nullable=False)
  event_place = db.Column(db.String(100), nullable=False)
  event_status = db.Column(db.String(20), nullable=False)

  def __init__(self, event_name, event_promo_info, event_date, event_time, event_place, event_status):
    self.event_name = event_name
    self.event_promo_info = event_promo_info
    self.event_date = event_date
    self.event_time = event_time
    self.event_place = event_place
    self.event_status = event_status
  
  def __repr__(self):
    return f"<Event {self.event_name} >"

db.create_all()
db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Browser caching issue
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response

def allowed_file(image):
    return '.' in image and \
           image.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
  categories = Category.query.all()
  menus = Menu.query.all()
  event = Event.query.filter_by(event_status="active").first()
  images_list = []
  for menu in menus:
    image_encode = base64.b64encode(menu.menu_image)
    image_decode = image_encode.decode("UTF-8")
    images_list.append(image_decode)
  return render_template("index.html",
    categories=categories,
    menus=menus, 
    images_list=images_list,
    event=event
  )
  
@app.route("/api/newsletter", methods=["POST"])
def add_newsletter():
  # Check request is json
  if request.is_json:
    req = request.get_json()
    firstname = req.get("firstname")
    lastname = req.get("lastname")
    email = req.get("email")
    # Validation
    if not firstname or not lastname or not email:
      return jsonify(message="Bad request!"), 400
    # Email Already Exist!
    find_email = Subscriber.query.filter_by(subscriber_email=email).first()
    if find_email:
      return jsonify(message="Email already exist!"), 409
    try:
      subscriber = Subscriber(firstname, lastname, email)
      db.session.add(subscriber)
      db.session.commit()
      return jsonify(message="Success"), 201
    except Exception as e:
      return jsonify(message=f"Something went wrong! {e}")
  else:
    return jsonify(message="Bad request, data is not a json!"), 400

@app.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    username = request.form["username"]
    password = request.form["password"]
    # get user
    try:
      user = User.query.filter_by(username=username).first()
      # print(user)
      # Check username and password login
      if user and check_password_hash(user.password, password):
        # print('passed!')
        # Passed
      #   # session["logged_in"] = True
      #   # session["username"] = username
        login_user(user)
        flash(f'Log in success ✔️. Hello {user.name.title()} 😄!', "success")
        return redirect(url_for("admin_dashboard"))
      else:
        flash("Login failed! ☹️ Invalid username or password", "danger")
        return redirect(url_for("login"))
    except Exception as e:
      flash(f"Something went wrong! {e}", "danger")
      return redirect(url_for("login"))
  # return render_template("login.html", form=form, login=True)
  return render_template('pages/login.html', form=form)

# #Check if the user logged in
# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if "logged_in" in session:
#           return f(*args, **kwargs)
#         else:
#           flash("Unauthorised ⛔, Please login!")
#           return redirect(url_for("login"))
#     return wrap

# Logout user
@app.route("/logout")
@login_required
def logout():
  session.clear()
  flash("Logged out! Bye 👋, have a nice day!", "success")
  return redirect(url_for("login"))

@app.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
  # categories = Category.query.all()
  # menus = Menu.query.all()
  # subscribers = Subscriber.query.all()
  # event = Event.query.filter_by(event_status="active").first()
  # events = Event.query.all()
  # count_subscribers = len(subscribers)
  # count_menus = len(menus)
  # # count_event = len(event)
  # count_all_events = len(events)
  # count_categories = len(categories)
  # total = {
  #   "subscribers" : count_subscribers,
  #   "menus" :  count_menus,
  #   "categories" : count_categories,
  #   "event" : event,
  #   "events" : count_all_events
  # }
  # return render_template("admin_dashboard/admin.html", total=total)
  return render_template("pages/admin.html")

@app.route("/admin_dashboard/subscriber")
@login_required
def subscriber():
   # Fetch all data in subscriber list
  data_subscriber = Subscriber.query.all()
  return render_template('admin_dashboard/subscriber.html', subscribers = data_subscriber)

@app.route("/admin_dashboard/category")
@login_required
def category():
  # Fetch all category data
  categories = Category.query.all()
  return render_template("admin_dashboard/category.html", categories = categories)

@app.route("/admin_dashboard/category/add", methods=["GET", "POST"])
@login_required
def category_add():
  if request.method == "POST":
    try:
      # Get form category value
      category = request.form["category"].lower()
      data = Category(category)
      db.session.add(data)
      db.session.commit()
      flash(f"Success ✔️, category {category.title()} has been added!")
      return redirect(url_for('category'))
    except:
      flash("There is an issue!")
      return redirect(url_for('category'))
  else:
    return render_template("admin_dashboard/category-add.html")

@app.route("/admin_dashboard/category/edit/<int:id>", methods=["GET","POST"])
@login_required
def category_edit(id):
  category = Category.query.filter_by(id=id).first()
  if request.method == "POST":
    try:
      # Get input value
      category.category_name = request.form["category"].lower()
      db.session.commit()
      flash(f"Success ✔️, {category.category_name.title()} has been updated!")
      return redirect(url_for("category"))
    except:
      flash("Sorry, there is an issue!")
      return redirect(url_for("category"))
  else:
    return render_template("admin_dashboard/category-edit.html", category=category)

@app.route("/admin_dashboard/category/delete/<id>", methods=["POST"])
@login_required
def category_delete(id):
  try:
    data = Category.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    flash(f"Success ✔️, category {data.category_name.title()} has been deleted!")
    return redirect(url_for("category"))
  except:
    flash("There is an issue!")
    return redirect(url_for("category"))
  
@app.route("/admin_dashboard/menu", methods=["GET"])
@login_required
def menu():
  menus = Menu.query.all()
  return render_template("admin_dashboard/menu.html", menus=menus)

@app.route("/admin_dashboard/menu/add", methods=["GET","POST"])
@login_required
def menu_add():
  # Get category menu
  categories = Category.query.all()
  if request.method == "POST":
    try:
      menu_name = request.form["menu_name"]
      menu_description = request.form["menu_description"]
      menu_category = request.form["menu_category"]
      menu_image = request.files["menu_image"]
      if not menu_image:
        flash("There is no image selected, please upload the image")
        return redirect(url_for("menu_add"))
      if menu_image and allowed_file(menu_image.filename):
        menu_secure_img = secure_filename(menu_image.filename)
        menu_mimetype = menu_image.mimetype
        # Add query to save data
        data = Menu(menu_name, menu_description, menu_image.read(), menu_mimetype, menu_secure_img, menu_category)
        db.session.add(data)
        db.session.commit()
        flash(f"Success ✔️! menu {menu_name.title()} 🥘 has been added to the list")
        return redirect(url_for('menu'))
      else:
        flash("Upps, sorry only upload 'png', 'jpg', 'jpeg' extensions are allowed!")
        return redirect(url_for("menu"))
    except Exception as e:
      flash(f"Oops! There is an issue! {e}")
      return redirect(url_for('menu'))
  return render_template("admin_dashboard/menu-add.html", categories=categories)

@app.route("/admin_dashboard/menu/edit/<int:id>", methods=["GET","POST"])
@login_required
def menu_edit(id):
  menu = Menu.query.filter_by(id=id).first()
   # Convert blob image into base64
  image_string = base64.b64encode(menu.menu_image)
  # Decode into utf-8
  image_string = image_string.decode("UTF-8")
  categories = Category.query.all()
  if request.method == "POST":
    if request.files["menu_image"] and allowed_file(request.files["menu_image"].filename):
      menu.menu_name = request.form["menu_name"]
      menu.menu_description = request.form["menu_description"]
      menu.category_id = request.form["menu_category"]
      menu.menu_image = request.files["menu_image"].read()
      menu.menu_mimetype = request.files["menu_image"].mimetype
      menu.menu_filename = secure_filename(request.files["menu_image"].filename)
      db.session.commit()
      flash(f"Success ✔️, menu {menu.menu_name} has been updated! ")
      return redirect(url_for("menu"))
    elif not request.files["menu_image"] :
      menu.menu_name = request.form["menu_name"]
      menu.menu_description = request.form["menu_description"]
      menu.category_id = request.form["menu_category"]
      db.session.commit()
      flash(f"Success ✔️, menu {menu.menu_name} has been updated! ")
      return redirect(url_for("menu"))
    else:
      flash("Sorry, only .png, .jpg, .jpeg extensions are allowed!")
      return redirect(url_for("menu")) 
  return render_template("admin_dashboard/menu-edit.html", menu=menu, categories=categories, image_string=image_string)

@app.route("/admin_dashboard/menu/detail/<int:id>")
@login_required
def menu_detail(id):
  menu = Menu.query.filter_by(id=id).first()
  # Convert blob image into base64
  image_string = base64.b64encode(menu.menu_image)
  # Decode into utf-8
  image_string = image_string.decode("UTF-8")
  return render_template("admin_dashboard/menu-detail.html", menu=menu, image_string=image_string)

@app.route("/admin_dashboard/menu/delete/<int:id>", methods=["POST"])
@login_required
def menu_delete(id):
  try:
    data = Menu.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    flash(f"Success ✔️, delete menu {data.menu_name.title()}!")
    return redirect(url_for("menu"))
  except:
    flash("There is an issue delete menu!")
    return redirect(url_for("menu"))

@app.route("/admin_dashboard/event", methods=["GET"])
@login_required
def event():
  #Fetch all data in event list
  events = Event.query.all()
  return render_template('admin_dashboard/event.html', events=events)

@app.route("/admin_dashboard/event/add", methods=["GET","POST"])
@login_required
def event_add():
  if request.method == "POST":
    try:
      event_name = request.form["event"]
      event_promo_info = request.form["promo_info"]
      event_date_end = request.form["date_end"]
      event_time_end = request.form["time_end"]
      event_place = request.form["event_place"]
      event = Event(event_name, event_promo_info, event_date_end, event_time_end, event_place, event_status = "not_set")
      db.session.add(event)
      db.session.commit()
      flash("Success ✔️, new event has been added to the list!")
      return redirect(url_for("event"))
    except:
      flash("Upps, there is an issue!")
      return redirect(url_for("event"))
  else:
    return render_template("admin_dashboard/event-add.html")
  
@app.route("/admin_dashboard/event/delete/<id>", methods=["POST"])
@login_required
def event_delete(id):
  try:
    event = Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    flash(f"Success ✔️, delete event !")
    return redirect(url_for("event"))
  except:
    flash("There is an issue!")
    return redirect(url_for("event"))

@app.route("/admin_dashboard/event/edit/<id>", methods=["GET", "POST"])
@login_required
def event_edit(id):
  event = Event.query.filter_by(id=id).first()
  # Count rows where event is active
  event_status = ["active", "not_set", "finished"]
  if request.method == "POST":
    event_active = Event.query.filter_by(event_status = "active").count()
    # If event active <= 1 user will be directed to event list
    event.event_name = request.form["event_name"]
    event.event_promo_info = request.form["event_promo_info"]
    event.event_date = request.form["event_date_end"]
    event.event_time = request.form["event_time_end"]
    event.event_place = request.form["event_place"]
    event.event_status = request.form["event_status"].lower()
    db.session.commit()
    flash(f"Success ✔️, event {event.event_name} has been updated!")
    return redirect(url_for("event"))
  else: 
    return render_template("admin_dashboard/event-edit.html", event=event, event_status=event_status)

if __name__ == "__main__":
  app.run(debug=True)