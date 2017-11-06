# -*- coding: utf-8 -*-
"""

This module get data from mongodb, run pca and svm to predict the TWE STOCK INDEX
Run:
        $ python example_google.py

Todo:
    * date ETL to run PCA
    * PCA ETL to run svm

"""

import pandas as pd
from pymongo import MongoClient

mc = MongoClient(host='10.128.112.181:7379', username='bass', password='F4mIfVIYGUBYBiQE', authSource='admin')
db = mc.baas
cursor = db["_Cache"].find()
df = pd.DataFrame(list(cursor))

# delete useless field
del df['_id']

print(df)
