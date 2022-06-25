from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  style_username = {"class": "animate__animated animate__zoomInLeft form-control", "placeholder" : "Username"}
  style_password = {"class": "animate__animated animate__zoomInRight form-control", "placeholder" : "Password"}
  style_button = {"class": "btn btn-primary btn-block animate__animated"}
  username = StringField("Username", validators=[DataRequired()], render_kw=style_username)
  password = PasswordField("Password", validators=[DataRequired()], render_kw=style_password)
  submit = SubmitField("Sign In", render_kw=style_button)
