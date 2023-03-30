from flask import Flask, render_template
import datetime
import requests


app = Flask(__name__)


@app.route("/")
def main_page():
    curr_year = datetime.datetime.now().year

    return render_template("index.html", year=curr_year)


@app.route("/guess/<name>")
def guess(name):
    age_endpoint = "https://api.agify.io"
    gender_endpoint = "https://api.genderize.io"

    response = requests.get(age_endpoint, params={"name": name})
    predicted_age = response.json()["age"]

    response = requests.get(gender_endpoint, params={"name": name})
    predicted_gender = response.json()["gender"]

    return render_template("index_project.html", name=name, age=predicted_age, gender=predicted_gender)

@app.route("/blog/<num>")
def get_blog(num):
    posts_endpoint = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(posts_endpoint)
    all_posts = response.json()
    print(num)

    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run()
