from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
import requests
from sqlalchemy import exc

MOVIE_DB_API_KEY = "d91b18d635fcb45c8d292bc4425ee66e"
SEARCH_MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap(app)

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies_project.db"
# initialize the app with the extension
db.init_app(app)


def find_movies(movie):
    params={
        "api_key": MOVIE_DB_API_KEY,
        "query": movie
    }

    response = requests.get(SEARCH_MOVIE_URL, params=params)
    movies_data = response.json()["results"]
    # movies = []
    # for movie in movies_data:
    #     movie_data = {"title": movie["original_title"], "id": movie["id"]}
    #     movies.append(movie_data)

    return movies_data


class AddForm(FlaskForm):
    title = StringField('Movie Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):

    rating = FloatField('Rating', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String, nullable=False)


# with app.app_context():
#     db.create_all()
#     movie = Movie(
#     title="Phone Booth",
#     year="2002",
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's" \
#                 " sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads " \
#                 "to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
#
#     db.session.add(movie)
#     db.session.commit()

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        title = form.title.data
        movies = find_movies(title)

        return render_template("select.html", movies=movies)

    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        try:
            db.session.add(new_movie)
            return db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

        return redirect(url_for("edit", id=new_movie.id))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    movie_id = request.args.get("movie_id")
    movie = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one()

    if form.validate_on_submit():
        movie.review = form.review.data
        movie.rating = form.rating.data
        db.session.commit()

        return "DONE"

    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete")
def delete():

    movie_id = request.args.get("movie_id")
    movie = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one()
    db.session.delete(movie)
    db.session.commit()

    return "Successfully Deleted"


if __name__ == '__main__':
    app.run(debug=True)
