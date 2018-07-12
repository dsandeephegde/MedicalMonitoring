from app import app
from sqlalchemy import create_engine
import pandas as pd
from flask_pymongo import PyMongo
from odo import odo
from flask import jsonify
import json
from bson import json_util
from bson.json_util import dumps, loads
import bson


app.config['MONGO_DBNAME'] = 'mm'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mm'

mongo = PyMongo(app)


def therapeutic_areas():
    # engine = create_engine('mysql+mysqlconnector://root:sql123@localhost:3306/medicalmonitoring')
    # data = pd.read_sql('''select * from therapeuticarea;''', con=engine)
    # return data
    therapeutic_area = mongo.db.therapeutic_area
    dataframe = pd.DataFrame(list(therapeutic_area.find()))
    return dataframe


def indications(ta_name):
    therapeutic_area = mongo.db.therapeutic_area
    ta = therapeutic_area.find_one({"name": ta_name})
    indications = mongo.db.indications
    dataframe = pd.DataFrame(list(indications.find({"ta_id": ta['_id']})))
    return dataframe


def projects(indication_name):
    indications = mongo.db.indications
    indication = indications.find_one({"name": indication_name})
    projects = mongo.db.projects
    dataframe = pd.DataFrame(list(projects.find({"indication_id": indication['_id']})))
    return dataframe


def studies(project_name):
    projects = mongo.db.projects
    project = projects.find_one({"name": project_name})
    studies = mongo.db.studies
    dataframe = pd.DataFrame(list(studies.find({"project_id": project['_id']})))
    return dataframe


def bulk_update():
    ae = mongo.db.ae
    # df = pd.DataFrame(list(ae.find()))
    # json_string = dumps(ae.find())
    # return json.dumps(list(ae.find()))
    d = list(ae.find())
    return json.dumps(d, default=json_util.default)
    # return jsonify(ae.find())
    # bulk = mongo.db.ae.initialize_unordered_bulk_op()
    # for index, row in df.iterrows():
    #     _id = row['_id']
    #     # new_value = row['y_pred']
    #     bulk.find({'_id': _id}).update_one({'$set': {'y_pred': 1}})
    # bulk.execute()
    # return df
