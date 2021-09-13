from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/db_coffeeshop"
app.config["SQL_TRACK_MODIFICATION"] = False

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/login_process", methods=["POST"])
def login_process():
  username = request.form.get("username")
  password = request.form.get("password")
  print(username,password)
  # return render_template("admin_dashboard/pages/index.html");
  return "ok"
  
  

# @app.route("/admin_dashboard")
# def admin_dashboard():
# return "admin"

# @app.route("/newsletter", methods=["POST"])
# def newsletter():
#   firstname = request.form.get["firstname"]
#   lastname = request.form.get["lastname"]
#   email = request.form.get["email"]
#   print(firstname,lastname,email)
#   return "ok"


if __name__ == "__main__":
  app.run(debug=True)