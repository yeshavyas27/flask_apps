from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "some secret string"

# for email validation, pip install wtforms[email] then only it will work
class LoginForm(FlaskForm):
    email = StringField(label='Enter your email_id', validators=[DataRequired(), Email()])
    password = PasswordField(label='Enter password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Submit")


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    email_admin= "admin@email.com"
    password_admin = "12345678"
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email == email_admin and password == password_admin:
            return render_template("success.html")
        else:
            return render_template("denied.html")

    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
