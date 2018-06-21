import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine


def split_data_table(table, train_data_percentage):
    engine = create_engine('mysql+mysqlconnector://root:sql123@localhost:3306/medicalmonitoring')
    df_ae_std = pd.read_sql('''select * from {}'''.format(table), con=engine)
    ae_train, ae_prod = train_test_split(df_ae_std, test_size=(1 - train_data_percentage))
    ae_train.to_sql('{}_train'.format(table), con=engine, if_exists='replace')
    ae_prod.to_sql('{}_prod'.format(table), con=engine, if_exists='replace')
