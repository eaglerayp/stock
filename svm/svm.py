# -*- coding: utf-8 -*-
"""

This module get data from mongodb, run pca and svm to predict the TWE STOCK INDEX
Run:
        $ python example_google.py

Todo:
    * run PCA
    * PCA ETL to run svm

"""

import numbers
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
from sklearn.decomposition import PCA
from sklearn import svm

# Get dataframe from mongodb

MONGO_CLIENT = MongoClient(host='127.0.0.1:27017')
STOCK_COLLECTION = MONGO_CLIENT.stock["TWSE"]
query_result = STOCK_COLLECTION.find(
    #filter= {'Date':{'$gt':20100000}},
    # limit=2000,
    projection={'Date': False,
                'NTD': False,
                'TWC00': False,
                '_id': False},
    sort=[('Date', pymongo.ASCENDING)])
target_field = 'TWA00'
raw_datas = list(query_result)
n = len(raw_datas)
print("Data count:", n)
# diffDay mins R+n
diffDay = 1
test_samples = 60
diff_datas = []
answers = []
for i in range(0 + diffDay, n, diffDay):
    diff_data = {}
    for k, v in raw_datas[i].items():
        if k == target_field:
            # no put target value int training data
            continue
        # use diff %
        vN = isinstance(v, numbers.Number)
        lastV = raw_datas[i - diffDay][k]
        lN = isinstance(lastV, numbers.Number)
        if vN and lN:
            diff_data[k] = (v - lastV) / lastV
        elif vN:
            diff_data[k] = 1
        else:
            diff_data[k] = 0
    diff_datas.append(diff_data)

# get labeled answer
for i in range(1 + diffDay, n, diffDay):
    v = raw_datas[i][target_field]
    lastV = raw_datas[i - diffDay][target_field]
    vN = isinstance(v, numbers.Number)
    lN = isinstance(lastV, numbers.Number)
    if vN and lN:
        diff = (v - lastV) / lastV
    elif vN:
        diff = 1
    else:
        diff = 0
    category = 0
    if diff > 0:
        category = 1
    answers.append(category)

# run PCA
data_frame = pd.DataFrame(diff_datas)
# print(data_frame[0:2])
pca_model = PCA(n_components=50)
pca_model.fit(data_frame)
pca_components = pca_model.explained_variance_ratio_
ratio = 0.0
for x in pca_components:
    ratio = ratio + x
print(ratio)
# print(pca_model.explained_variance_ratio_)

reduced_datas = pca_model.transform(data_frame)

# run SVC (classifier)
# use reduced_data and test result pair to svm
# rdf[0] + tR[0]
trained_data = reduced_datas[:-test_samples - 1]
trained_answer = answers[:-test_samples]
assert len(trained_data) == len(trained_answer)
print("traind data count:", len(trained_data))

# train svm
svc_model = svm.SVC()
svc_model.fit(trained_data, trained_answer)
print("training data precision:", svc_model.score(trained_data, trained_answer))

print("precision by score:", svc_model.score(
    reduced_datas[-test_samples - 1:-1], answers[-test_samples:]))


# put array of testing training data (reduced)
predicts = svc_model.predict(reduced_datas[-test_samples - 1:])
print("Predicts:", predicts)
correct = 0
answer_true = 0
predict_true = 0
for i in range(0, test_samples, 1):
    ni = (-test_samples + i)
    answer_true = answer_true + answers[ni]
    predict_true = predict_true + predicts[i]
    if predicts[i] == 1 and answers[ni] == 1:
        correct = correct + 1
# get precision and recall metrics
print("correct:", correct)
print("predict_true:", predict_true)
print("answer_true:", answer_true)
precision = correct / predict_true
recall = correct / answer_true
print("precision:", precision)
print("recall:", recall)
print("next predict:", predicts[-1])
