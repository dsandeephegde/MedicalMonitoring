import sys
import pandas as pd
import pymongo
import json


def import_content(file_path, collection_name):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['mm']
    db_cm = mng_db[collection_name]

    data = pd.read_csv(file_path, encoding ='latin1')
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)


if __name__ == "__main__":
    filepath = sys.argv[1]
    collection_name = sys.argv[2]
    import_content(filepath, collection_name)
