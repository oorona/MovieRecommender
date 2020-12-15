import json
import os
import pandas as pd
import numpy as np
import scipy
import random
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity


basedata="./recommenderapp/static/data"


movies=pd.read_feather(os.path.join(basedata,'movies.feather'))
movies["ID"]=movies.MovieID
movies=movies.set_index("MovieID")
top=20
categories=pd.read_feather(os.path.join(basedata,'categories.feather'))
genresmatrix=pd.read_feather(os.path.join(basedata,'genresmatrix.feather'))
genresmatrix=genresmatrix.set_index("MovieID") 
similarityMatrix=pd.read_feather(os.path.join(basedata,'similarity.feather')).to_numpy(np.float16)


def getvalidMovies():
    valid_movies=pd.read_feather(os.path.join(basedata,'validmovies.feather'))
    return valid_movies['MovieID'].to_numpy()

def getGlobalAve():
    #ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    #ratings_movies=ratings_movies.set_index("MovieID")
    return  3.581564453029317

def getMapIdDictRows(df):
    mapiddict={}
    j=0
    for i in df.index:
        mapiddict[i]=j
        j+=1
    return mapiddict,df.shape[0]


def getBestByCategory(category,topn=20):
   
    topn=genresmatrix[category].sort_values(ascending=False)[:topn]
    topnlist=list(topn.index)
    return json.loads(movies.loc[topnlist].to_json(orient='records'))

def getCategories():
    return json.loads(categories.to_json(orient='records'))

def getSelectionList(topn=20):
    ids=random.sample(range(0, len(validMovies)), topn)
    #print(ids)
    #for i in ids:
    #    print(i,movies.iloc[i])        

    print(movies[movies['ID'].isin(ids)][['Title','ID']])
    return json.loads(movies[movies['ID'].isin(ids)].to_json(orient='records'))

def getMapIdDictCols():
    mapiddict={}
    j=0
    for i in validMovies:
        mapiddict[i]=j
        j+=1
    return mapiddict,len(validMovies)

def getUserQueryVector(userQuery):
    mapiddict,size=getMapIdDictCols()
    result=np.full(size,np.nan)
    for i in userQuery:
        result[mapiddict[i]]=userQuery[i]
    return result




def getSimilary(utilityMatrix,index):
        item1=utilityMatrix[index]
        item1=item1 - np.nanmean(item1)
        item1=np.nan_to_num(item1)
        distance=np.zeros(utilityMatrix.shape[0])
        for i in range(utilityMatrix.shape[0]): 
            item=utilityMatrix[i] -np.nanmean(utilityMatrix[i])
            item=np.nan_to_num(item)
            r=1-spatial.distance.cosine(item1,item)
            distance[i]=r
        return distance


def getUserPredictions(queryVector,k):    
    for i in range(len(queryVector)):        
        if np.isnan(queryVector[i]):
                vectorSimilarity=similarityMatrix[i]
                #print(vectorSimilarity)
                r=getRatingIBCF(queryVector,vectorSimilarity,k,debug=False)
                #print(r)
                queryVector[i]=r
    return queryVector   


def getRatingIBCF(colUtilityMatrix,rowSimilarityMatrix,top,debug=False):
    row=rowSimilarityMatrix

    col=colUtilityMatrix
    mask=~np.isnan(col)
    
    simrow=np.multiply(row,col)
    simcol=np.multiply(row,mask)
    
    validrow=simrow[mask]
    validcol=simcol[mask]
    
    sortedvalues=np.argsort(validcol)
    topn=sortedvalues[-top:]
    dt=np.sum(validrow[topn])
    db=np.sum(np.abs(validcol[topn]))
    result=(dt/db)
    return(result)   




def getRecommendations(userQuery,topn,k):
    #ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    #ratings_movies=ratings_movies.set_index("MovieID")
    #utilityMatrix=ratings_movies.to_numpy()
    print("Size of the array: ", similarityMatrix.size/1e6) 
    print("Memory size of one array element in bytes: ", similarityMatrix.itemsize) 
    print("Memory size of numpy array in bytes:", similarityMatrix.size * similarityMatrix.itemsize)
    print('matrixsize ',similarityMatrix.shape)

    print(userQuery)
    for i in userQuery:
        print(i,movies.loc[i]['Title'])
    queryVector=getUserQueryVector(userQuery)

    #queryVector=getUserPredictions(utilityMatrix,queryVector,k)       
    queryVector=getUserPredictions(queryVector,k)   
    print (queryVector)
    queryindex=np.argsort(queryVector)
    topmovies=queryindex[-topn:]
    return json.loads(movies.iloc[topmovies].to_json(orient='records'))




validMovies=getvalidMovies()  
