from flask import Flask, render_template,url_for,send_from_directory
import requests

from . import app
from . import recommender


movies = [
    {
        'title':"Toy Story",
        'year':"1995",
        'filename':"images/movies/1.jpg"
    },
    {
        'title':"Jumanji",
        'year':"1995",
        'filename': "images/movies/2.jpg"
    }
]
categories = [
    {
        'name':"Action"
    },
    {
        'name':'Horror'
    },
    {   
        'name':'Suspense'
    }
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/genres/")
def genres():
    category="Action"   
    movies=recommender.getBestByCategory(category)
    return render_template("genres.html",categories=categories)

@app.route("/results/")
def results():
    category="Action"   
    movies=recommender.getBestByCategory(category)
    return render_template("results.html",movies=movies)    

@app.route("/recommendations/")
def recommendations():
    return render_template("recommendations.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

