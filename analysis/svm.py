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
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn import svm

# Get dataframe from csv
path = './data/car.twseelec.csv'
datas = pd.read_csv(path, header=0)

target_field = 'GENERAL INTERFAC'
diffDay = 1
test_samples = 60
answers = []
for i in range(0, len(datas), 1):
    if datas['GENERAL INTERFAC'][i] > 0:
        answers.append(1)
    else:
        answers.append(-1)


# print(data_frame[0:2])
pca_model = PCA(n_components='mle', svd_solver='full')
pca_model.fit(scale(datas))
pca_components = pca_model.explained_variance_ratio_
ratio = 0.0
for x in pca_components:
    ratio = ratio + x
print("cum ratio:", ratio)
for x in range(0, 5, 1):
    print(x, " component ratio:", pca_components[x])
# print(pca_model.explained_variance_ratio_)

reduced_datas = pca_model.transform(datas)

# # run SVC (classifier)
# # use reduced_data and test result pair to svm
# # rdf[0] + tR[0]
trained_data = reduced_datas[:-test_samples - 1]
trained_answer = answers[1:-test_samples]
assert len(trained_data) == len(trained_answer)
print("traind data count:", len(trained_data))
print(trained_answer)
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
