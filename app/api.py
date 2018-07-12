from app import app
from app import mysql
from flask import request
import pandas as pd
from app import AEModels
from sqlalchemy import create_engine
from app import filters


@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    # cursor.execute('''select * from ae''')
    # data = pd.DataFrame(cursor.fetchall())
    engine = create_engine('mysql+mysqlconnector://root:sql123@localhost:3306/medicalmonitoring')
    data = pd.read_sql('''select * from ae''', con=engine)
    # data.to_sql('ae', con=engine, if_exists='replace')
    for i, row in data.iterrows():
        # print('update medicalmonitoring.ae set y_pred={} where USUBJID={};'.format(row['y_pred'], row['USUBJID']))
        cursor.execute('update ae set y_pred={} where USUBJID={}'.format(row['y_pred'], row['USUBJID']))
    if data is None:
        return "Username or Password is wrong"
    else:
        return "working"


@app.route('/ae/lof', methods=['POST'])
def lof():
    request_json = request.get_json()
    data = AEModels.lof(request_json['table'], request_json['tests'])
    return data.to_json()


@app.route('/therapeutic_areas', methods=['GET'])
def therapeutic_areas():
    data = filters.therapeutic_areas()
    return data.to_json(default_handler=str, orient='records')


@app.route('/indications', methods=['GET'])
def indications():
    ta_name = request.args['ta']
    data = filters.indications(ta_name)
    return data.to_json(default_handler=str, orient='records')


@app.route('/projects', methods=['GET'])
def projects():
    indication = request.args['indication']
    data = filters.projects(indication)
    return data.to_json(default_handler=str, orient='records')


@app.route('/studies', methods=['GET'])
def studies():
    project = request.args['project']
    data = filters.studies(project)
    return data.to_json(default_handler=str, orient='records')


@app.route('/bulk_update', methods=['GET'])
def bulk_update():
    # data = filters.bulk_update()
    # return data.to_json(default_handler=str, orient='records')
    return filters.bulk_update()
