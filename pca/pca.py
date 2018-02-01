# -*- coding: utf-8 -*-
"""

This module get data from mongodb, run pca and svm to predict the TWE STOCK INDEX
Run:
        $ python example_google.py

Todo:
    *

"""


from sklearn.preprocessing import scale
import pandas as pd
from sklearn.decomposition import PCA

# Read csv file
path = './data/car.twseelec.csv'
datas = pd.read_csv(path, header=0)

print(datas['GENERAL INTERFAC'])


# run PCA

pca_model = PCA(n_components='mle', svd_solver='full')
pca_model.fit(scale(datas))
pca_components = pca_model.explained_variance_ratio_
ratio = 0.0
for x in range(0, 50, 1):
    ratio = ratio + pca_components[x]
    print("cum ratio:", x + 1, ";", ratio)
print("PCA component:", len(pca_components))

print(pca_components[:10])
print(pca_model.singular_values_[:10])
# print(pca_model.n_features_)
# print(pca_model.n_samples_)
# print(pca_model.components_)
