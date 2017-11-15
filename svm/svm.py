# -*- coding: utf-8 -*-
"""

This module get data from mongodb, run pca and svm to predict the TWE STOCK INDEX
Run:
        $ python example_google.py

Todo:
    * run PCA
    * PCA ETL to run svm

"""

import pandas as pd
import numbers
import pymongo
from pymongo import MongoClient
from sklearn.decomposition import PCA
from sklearn import svm
from IPython.display import display

# Get dataframe from mongodb

mc = MongoClient(host='127.0.0.1:27017')
db = mc.stock
cursor = db["TWSE"].find(limit=1000,projection={'Date':False,'_id':False},sort=[('Date',pymongo.ASCENDING)])
target = 'TWA00'
datas = list(cursor)
n = len(datas)
print("Data count:",n)
# diffDay mins R+n
diffDay = 1
postData = []
answer = []
for i in range(0+diffDay,n,diffDay):
    diffData = {}
    for k,v in datas[i].items():
        if k == target:
            # no put target value int training data
            continue
        # try use diff % ?
        if not isinstance(v, numbers.Number):
            v = 0
        lastV = datas[i-diffDay][k]
        if not isinstance(lastV, numbers.Number):
            lastV = 0
        diffData[k] = v - lastV
    postData.append(diffData)

# get labeled answer
for i in range(1+diffDay,n,diffDay):
    v = datas[i][target]
    lastV = datas[i-diffDay][target]
    if not isinstance(v, numbers.Number):
        v = 0
    if not isinstance(lastV, numbers.Number):
        lastV = 0
    diff = v - lastV
    category = 0
    if diff > 0.0:
        category = 1
    answer.append(category)

# get time diff by iterating through cursor
df = pd.DataFrame(postData)
# # delete useless field
# del df['_id']

# print(df)

# handle nan value

# run PCA
pca = PCA(n_components=500)
pca.fit(df)
print(pca.explained_variance_ratio_)

reduced_data = pca.transform(df)
dataLen = len(reduced_data)
rdf = pd.DataFrame(reduced_data)
#display(rdf)

# run SVC (classifier)
# use reduced_data and test result pair to svm
# rdf[0] + tR[0]
svcModel = svm.SVC()
svcModel.fit(rdf[:-1],answer)

# put array of testing training data (reduced)
print(svcModel.predict(reduced_data))

# get a list of result
# 0~-1 is trainging data