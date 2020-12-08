import json

import pandas as pd

genresmatrix=pd.read_feather('./static/genresmatrix.feather')
genresmatrix=genresmatrix.set_index("MovieID")
movies=pd.read_feather('./static/movies.feather')
movies=movies.set_index("MovieID")
categories=pd.read_feather('./static/categories.feather')
top=20

def getBestByCategory(category):
    print(category)
    topn=genresmatrix[category].sort_values(ascending=False)[:20]
    topnlist=list(topn.index)
    print(topnlist)
    return json.loads(movies.loc[topnlist].to_json(orient='records'))

def getCategories():
    return json.loads(categories.to_json(orient='records'))
