import json
import os
import pandas as pd
import numpy as np
import scipy
from sklearn.metrics.pairwise import cosine_similarity


basedata="./recommenderapp/static/data"


movies=pd.read_feather(os.path.join(basedata,'movies.feather'))
movies["ID"]=movies.MovieID
movies=movies.set_index("MovieID")
top=20



def getMapIdDictRows(df):
    mapiddict={}
    j=0
    for i in df.index:
        mapiddict[i]=j
        j+=1
    return mapiddict,df.shape[0]


def getBestByCategory(category,topn=20):
    genresmatrix=pd.read_feather(os.path.join(basedata,'genresmatrix.feather'))
    genresmatrix=genresmatrix.set_index("MovieID")    
    topn=genresmatrix[category].sort_values(ascending=False)[:topn]
    topnlist=list(topn.index)
    return json.loads(movies.loc[topnlist].to_json(orient='records'))

def getCategories():
    categories=pd.read_feather(os.path.join(basedata,'categories.feather'))
    return json.loads(categories.to_json(orient='records'))

def getSelectionList(topn=20):
    ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    ratings_movies=ratings_movies.set_index("MovieID")    
    selection=ratings_movies.sample(n=topn)
    ids=selection.index.to_numpy()
    print(ids)
    #for i in ids:
    #    print(i,movies[movies.ID.isin[i]])        

    print(movies[movies['ID'].isin(ids)][['Title','ID']])
    return json.loads(movies[movies['ID'].isin(ids)].to_json(orient='records'))



def getRatingIBCF(utilityMatrix,similarityMatrix,rowid,colid,top,globalave,debug=False):
    row=similarityMatrix[rowid]    
    aveuser=np.nanmean(utilityMatrix[:,colid])
    col=utilityMatrix[:,colid]-aveuser
    mask=~np.isnan(col)
    
    simrow=np.multiply(row,col)
    simcol=np.multiply(row,mask)
    simcol[rowid]=np.nan
    
    validrow=simrow[mask]
    validcol=simcol[mask]
    
    sortedvalues=np.argsort(validrow)
    topn=sortedvalues[-top:]
    dt=np.sum(validrow[topn])
    db=np.sum(np.abs(validcol[topn]))
    result=(dt/db)+aveuser
    if np.isnan(result):
        if np.isnan(aveuser):
            result=globalave
        else:
            result=aveuser
    
    return(result)    

def getSimilarityMatrix(utilityDataFrame):
    # Calculates the mean for each row
    rowMean=utilityDataFrame.mean(1,True).to_numpy(np.float16)
    # Convers  the array to a matrix
    matrixRowMean=rowMean.reshape(-1,1)
    # Data Frame is converted into matrix sparce matrix
    utilityMatrix=utilityDataFrame.to_numpy(np.float16)
    utilityMatrixSparse = scipy.sparse.csc_matrix(utilityMatrix)
    # Each non Nan are substract the mean of the row.
    utilityMatrixCenter=utilityMatrixSparse-matrixRowMean
    # All Nan alements are converted to zero
    utilityMatrixCenterZero=np.nan_to_num(utilityMatrixCenter)
    # Cosine similarity matrix is calculated
    SimilarityMatrix = cosine_similarity(utilityMatrixCenterZero)
    return SimilarityMatrix        


def getUserQueryVector(userQuery,mapiddict,size):
    result=np.full(size,np.nan)
    for i in userQuery:
        result[mapiddict[i]]=userQuery[i]
    return result

def getMapIdDictCols(df):
    mapiddict={}
    j=0
    for i in df.columns:
        mapiddict[i]=j
        j+=1
    return mapiddict,df.shape[1]




def getUserPredictions(utilityMatrix,queryVector,size,k,globalave):    

    if utilityMatrix.shape[1] == size+1:        
        utilityMatrix[size]=queryVector
    else:
        utilityMatrix=np.append(utilityMatrix,queryVector.reshape(-1,1),axis=1)
    similarityMatrix=getSimilarityMatrix(pd.DataFrame(utilityMatrix))   
    for i in range(len(queryVector)):        
        if np.isnan(queryVector[i]):
                r=getRatingIBCF(utilityMatrix,similarityMatrix,i,size+1,k,globalave,debug=False)
                queryVector[i]=r
    return queryVector

def getUtilityMatrix():
    ratings_movies=pd.read_feather(os.path.join(basedata,'utilitymatrix.feather'))
    ratings_movies=ratings_movies.set_index("MovieID")
    globalave=np.nanmean(ratings_movies)
    mapiddict,size=getMapIdDictRows(ratings_movies)
    utilityMatrix=ratings_movies.to_numpy()
    return utilityMatrix,mapiddict,size,globalave

def getRecommendations(userQuery,topn,k):
    utilityMatrix,mapiddict,size,globalave=getUtilityMatrix()
    print(userQuery)
    for i in userQuery:
        print(i,movies.loc[i]['Title'])
    queryVector=getUserQueryVector(userQuery,mapiddict,size)
    queryVector=getUserPredictions(utilityMatrix,queryVector,size,k,globalave)       
    queryindex=np.argsort(queryVector)
    topmovies=queryindex[-topn:]
    return json.loads(movies.iloc[topmovies].to_json(orient='records'))