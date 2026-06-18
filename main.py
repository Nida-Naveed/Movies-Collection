from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
#
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzY2RkZmJlYThhOTc0NmZiZTI5NzhlNDA2MmU3ZjkyMCIsIm5iZiI6MTc3NjcwNjEyOC41MDEsInN1YiI6IjY5ZTY2MjUwYzA1MjgwOTBiMjg0Zjg5OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ym4R-EriR1fMv1UqDF01l4CPxeSynEZ49o2CmaYjkYs"
}

#app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-db.sqlite'
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    __tablename__ = 'movies'
    id: Mapped[Integer]=mapped_column(Integer, primary_key=True)
    title: Mapped[String] =mapped_column(String(250),unique=True, nullable=False)
    year: Mapped[String] = mapped_column(String(250), nullable=False)
    description: Mapped[String] = mapped_column(String(250), nullable=False)
    rating: Mapped[Float] = mapped_column(Float, nullable=False)
    ranking: Mapped[Integer] = mapped_column(Integer, nullable=False)
    review: Mapped[String] = mapped_column(String(250), nullable=False)
    img_url: Mapped[String] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

#add to the movie list
first_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)
second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)

@app.route("/")
def home():
    #add movies to the database created
    # with app.app_context():
    #         db.session.add_all([first_movie, second_movie])
    #         db.session.commit()
    with app.app_context():
        result = db.session.execute(db.select(Movie))
        all_movies = result.scalars().all()

    sorted_movies = sorted(all_movies, key=lambda movie: movie.ranking)
    return render_template("index.html", all_movies= sorted_movies)

class MovieForm(FlaskForm):
    ranking = FloatField('Ranking', validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Done")

@app.route("/delete/<movie_title>")
def delete(movie_title):
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.title == movie_title)).scalar()
        db.session.delete(movie)
        db.session.commit()
        print("Movie deleted: ", movie_title)
        return redirect(url_for("home"))

@app.route("/edit/<movie_title>", methods=["GET", "POST"])
def edit(movie_title):
    form = MovieForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with app.app_context():
                movie = db.session.execute(db.select(Movie).where(Movie.title==movie_title)).scalar()
                movie.ranking = request.form.get("ranking")
                movie.review = request.form.get("review")
                db.session.commit()
                print(movie.title,"Movie edited")
                return redirect(url_for("home"))
    return render_template("edit.html", form=form)

class Add_movie(FlaskForm):
    title = StringField("Title of your movie:", validators=[DataRequired()])
    submit = SubmitField("Add")

@app.route("/add", methods=["GET", "POST"])
def add():
    form = Add_movie()
    if request.method == "POST":
        if form.validate_on_submit():

            return  redirect(url_for("select", search_title=form.title.data))
    return render_template("add.html",form=form)

@app.route("/select/<string:search_title>")
def select(search_title):
    url = f"https://api.themoviedb.org/3/search/movie?query={search_title}&include_adult=false&language=en-US&page=1"
    response = requests.get(url, headers=headers)
    response = response.json()
    print("Search Results:")
    for movie in response["results"]:
        print(movie["title"])
    return render_template("select.html",response=response)

@app.route("/add_movie/<int:movie_id>")
def movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(url, headers=headers)
    data = response.json()

    new_movie = Movie(
        title=data["title"],
        year=data["release_date"].split("-")[0],
        description=data["overview"],
        rating=data["vote_average"],
        ranking=0,
        review="",
        img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    print("Movie added:")
    print(data["title"])
    return redirect(url_for("edit", movie_title=data["title"]))

if __name__ == '__main__':
    app.run(debug=True)

