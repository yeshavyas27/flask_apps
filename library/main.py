from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from markupsafe import escape
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "LALALLAA"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Add_Book_Form(FlaskForm):
    book_name = StringField('Book name: ', validators=[DataRequired()])
    book_author = StringField('Author name: ', validators=[DataRequired()])
    book_rating = IntegerField('Book Rating: ', validators=[DataRequired()])


class RatingEditForm(FlaskForm):
    book_rating = IntegerField('Book Rating: ', validators=[DataRequired()])


with app.app_context():
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.Float, nullable=False)

        # Optional: this will allow each book object to be identified by its title when printed.
        def __repr__(self):
            return f'<Book {self.title}>'


    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        # it gives a list of book objects
        all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = Add_Book_Form()
    if form.validate_on_submit():
        with app.app_context():
            new_book = Book(title=form.book_name.data, author=form.book_author.data, rating=form.book_rating.data)
            db.session.add(new_book)
            db.session.commit()

        return "<h1>Success</h1>"

    return render_template("add.html", form=form)


@app.route("/edit/<book_title>", methods=["GET", "POST"])
def edit(book_title):
    form = RatingEditForm()
    title = format(escape(book_title))
    book = db.session.execute(db.select(Book).filter_by(title=title)).scalar_one()

    if form.validate_on_submit():
        book.rating = form.book_rating.data
        db.session.commit()

        return "<h1>Success</h1>"

    return render_template("edit.html", form=form, book=book)


@app.route("/delete/<book_title>", methods=["GET", "POST"])
def delete(book_title):
    title = format(escape(book_title))
    book = db.session.execute(db.select(Book).filter_by(title=title)).scalar_one()
    db.session.delete(book)
    db.session.commit()

    return "<h1>Succesfully deleted</h1>"


if __name__ == "__main__":
    app.run()
