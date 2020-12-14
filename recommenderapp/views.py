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
    topn=int(request.args.get('topn'))
    movies=recommender.getBestByCategory(category,topn)
    
    return render_template("results.html",movies=movies,category=category)    

@app.route("/recommendations/", methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        #print("Post received new")
        #print(len(request.args))
        for i in request.args:
            print(i)
        return render_template("inputselections.html")   
    else:
        categories=recommender.getCategories()
        return render_template("recommendations.html",categories=categories)

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/listselection/")
def listselection():
    topn=int(request.args.get('topn'))
    movies=recommender.getSelectionList(topn)    
    return render_template("selectionlist.html",movies=movies)   

@app.route("/inputselection/", methods=['GET', 'POST'])
def inputselection():    
    topn=10
    k=10
    if request.method == 'GET':
        moviequery={}
        #print("Post received")
        #print(len(request.args))
        for i in request.args:
            #print(i+" "+request.args.get(i))
            moviequery[int(i[6:])]=int(request.args.get(i))
    #print(moviequery)
    movies=recommender.getRecommendations(moviequery,topn,k)    
    return render_template("resultsr.html",movies=movies)   