import requests
from flask import Flask, render_template, request, send_from_directory, url_for

from . import app, recommender


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/genres/")
def genres():
    categories=recommender.getCategories()
    return render_template("genres.html",categories=categories)

@app.route("/results/")
def results():
    category=request.args.get('category')  
    movies=recommender.getBestByCategory(category)
    return render_template("results.html",movies=movies)    

@app.route("/recommendations/")
def recommendations():
    return render_template("recommendations.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

