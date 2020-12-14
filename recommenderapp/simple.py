import requests
from requests.compat import urljoin
import json
import pandas as pd
import io
import re
import numpy as np
import warnings
import numpy as np
import os
import scipy
from scipy.sparse.linalg import svds
from scipy import spatial
import sklearn.preprocessing as pp
from sklearn.metrics.pairwise import cosine_similarity
import time
import sys
import math

basedata="./recommenderapp/static/data"


ratings_movies=pd.DataFrame(np.array(
    [[1,np.nan,3,np.nan,np.nan,5,np.nan,np.nan,5,np.nan,4,np.nan],
    [np.nan,np.nan,5,4,np.nan,np.nan,4,np.nan,np.nan,2,1,3],
    [2,4,np.nan,1,2,np.nan,3,np.nan,4,3,5,np.nan],
    [np.nan,2,4,np.nan,5,np.nan,np.nan,4,np.nan,np.nan,2,np.nan],
    [np.nan,np.nan,4,3,4,2,np.nan,np.nan,np.nan,np.nan,2,5],
    [1,np.nan,3,np.nan,3,np.nan,np.nan,2,np.nan,np.nan,4,np.nan]]
    ))




def getGlobalAve():
    #ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    #ratings_movies=ratings_movies.set_index("MovieID")
    return  3.581564453029317


def getvalidMovies():
    ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    return ratings_movies['MovieID'].to_numpy()

def getUtilityMatrix():
    #ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    #ratings_movies=ratings_movies.set_index("MovieID")
    #utilityMatrix=csr_matrix(pd.read_feather(os.path.join(basedata,'utilitymatrix.feather')).to_numpy())
    #print( 'dense : {:0.2f} mbytes'.format(ratings_movies.memory_usage().sum() / 1e6))
    return ratings_movies.to_numpy()


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


def getUserPredictions2(queryVector,k):    
    for i in range(len(queryVector)):        
        if np.isnan(queryVector[i]):
                vectorSimilarity=getSimilary(utilityMatrix,i)
                r=getRatingIBCF2(queryVector,vectorSimilarity,k,debug=False)
                queryVector[i]=r
    return queryVector   


def getRatingIBCF2(colUtilityMatrix,rowSimilarityMatrix,top,debug=False):
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
    #if np.isnan(result):
    #    if np.isnan(aveuser):
    #        result=globalave
    #    else:
    #        result=aveuser
    return(result)      


globalave=getGlobalAve()  
validMovies=getvalidMovies()  
utilityMatrix=getUtilityMatrix()
queryVector=utilityMatrix[:,4]

print(getUserPredictions2(queryVector,2))