from flask import Flask, render_template, request, redirect, url_for
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
  if username == "admin" and password == "admin123":
    return redirect(url_for("admin_dashboard"))
  else:
    print("password or username is invalid!");
    return redirect(url_for("login"))
    
@app.route("/admin_dashboard")
def admin_dashboard():
  return "hello admin"

if __name__ == "__main__":
  app.run(debug=True)