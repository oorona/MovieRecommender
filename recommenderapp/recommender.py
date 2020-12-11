import json
import os
import pandas as pd
import numpy as np

basedata="./recommenderapp/static/data"

genresmatrix=pd.read_feather(os.path.join(basedata,'genresmatrix.feather'))
genresmatrix=genresmatrix.set_index("MovieID")
movies=pd.read_feather(os.path.join(basedata,'movies.feather'))
movies["ID"]=movies.MovieID
movies=movies.set_index("MovieID")
categories=pd.read_feather(os.path.join(basedata,'categories.feather'))
top=20

def getBestByCategory(category,topn=20):
    topn=genresmatrix[category].sort_values(ascending=False)[:topn]
    topnlist=list(topn.index)
    return json.loads(movies.loc[topnlist].to_json(orient='records'))

def getCategories():
    return json.loads(categories.to_json(orient='records'))

def getSelectionList(topn=20):
    return json.loads(movies.sample(n=topn).to_json(orient='records'))