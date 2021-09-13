from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/db_coffeeshop"
app.config["SQL_TRACK_MODIFICATION"] = False

@app.route("/", methods=["GET", "POST"])
def index():
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

if __name__ == "__main__":
  app.run(debug=True)