import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import LocalOutlierFactor
from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import precision_recall_curve, brier_score_loss, precision_score, recall_score, f1_score
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from app import mysql

le = LabelEncoder()
le_aesdth = LabelEncoder()
le_aeslife = LabelEncoder()
le_aehosp = LabelEncoder()
le_aesdisab = LabelEncoder()
le_aesmie = LabelEncoder()
le_aeterm = LabelEncoder()
le_aemodify = LabelEncoder()
le_aeacn = LabelEncoder()
le_aeout = LabelEncoder()
le_aeser = LabelEncoder()

accuracy = [0, 0, 0]


def encode_labels(data):
    data['AESDTH'] = le_aesdth.fit_transform(data.AESDTH.astype(str))
    data['AESLIFE'] = le_aeslife.fit_transform(data.AESLIFE.astype(str))
    data['AEHOSP'] = le_aehosp.fit_transform(data.AEHOSP.astype(str))
    data['AESDISAB'] = le_aesdisab.fit_transform(data.AESDISAB.astype(str))
    data['AESMIE'] = le_aesmie.fit_transform(data.AESMIE.astype(str))
    data['AETERM'] = le_aeterm.fit_transform(data.AETERM.astype(str))
    data['AEMODIFY'] = le_aemodify.fit_transform(data.AEMODIFY.astype(str))
    data['AEACN'] = le_aeacn.fit_transform(data.AEACN.astype(str))
    data['AEOUT'] = le_aeout.fit_transform(data.AEOUT.astype(str))
    data['AESER'] = le_aeser.fit_transform(data.AESER.astype(str))
    return data


def decode_labels(data):
    data['AESDTH'] = le_aesdth.inverse_transform(data.AESDTH)
    data['AESLIFE'] = le_aeslife.inverse_transform(data.AESLIFE)
    data['AEHOSP'] = le_aehosp.inverse_transform(data.AEHOSP)
    data['AESDISAB'] = le_aesdisab.inverse_transform(data.AESDISAB)
    data['AESMIE'] = le_aesmie.inverse_transform(data.AESMIE)
    data['AETERM'] = le_aeterm.inverse_transform(data.AETERM)
    data['AEMODIFY'] = le_aemodify.inverse_transform(data.AEMODIFY)
    data['AEACN'] = le_aeacn.inverse_transform(data.AEACN)
    data['AEOUT'] = le_aeout.inverse_transform(data.AEOUT)
    data['AESER'] = le_aeser.inverse_transform(data.AESER)
    return data


def lof(table_name, tests):
    engine = create_engine('mysql+mysqlconnector://root:sql123@localhost:3306/medicalmonitoring')
    data = pd.read_sql('''select * from {}'''.format(table_name), con=engine)
    data = data.fillna('N')
    data = encode_labels(data)
    clf = LocalOutlierFactor(n_neighbors=42)
    y_pred = clf.fit_predict(data.loc[:, tests])
    data['y_pred'] = y_pred
    cursor = mysql.connection.cursor()
    for i, row in data.iterrows():
        cursor.execute('''update {} set y_pred=%s where ID=%s;'''.format(table_name), (row['y_pred'], row['ID']))
    mysql.connection.commit()
    return data
