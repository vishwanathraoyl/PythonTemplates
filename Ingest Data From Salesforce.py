import pandas as pd
import re
import numpy as np
import sqlalchemy as sa
import pyodbc
from collections import OrderedDict as odict
from json import loads, dumps
import time

#Set up salesforce bulk API connection
from simple_salesforce import Salesforce
sf = Salesforce(
username='Userid', 
password='pwd',
security_token = 'token')

#Get Fields from SOQL query in salesforce
desc = sf.Account.describe()
field_names = [field['name'] for field in desc['fields']]
sf_acc  = sf.query_all("select * from Table where Column in ('Condition') ")


#Organize dicts and separate and normalize dictionaries to relational table
def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))

a = to_dict(sf_acc)
a = to_dict(a)

records = a.values()
records = a['records']
data = {}


for rec in records:
    for k, v in rec.items():
        if k == 'attributes':
            continue
        data.setdefault(k, []).append(v)

#Create dataframe
Data = pd.DataFrame(data)

#Store in S3 bucket
s3_url = 's3://bucket/folder/bucket.parquet.gzip'
Data.to_parquet(s3_url, compression='gzip')

time.sleep(10)

#Create SQL connection
engine = sa.create_engine('mssql+pyodbc://Server/DB1?driver=SQL+Server+Native+Client+11.0',fast_executemany=True)

#Read Parquet from S3
Data = pd.read_parquet(s3_url, engine='fastparquet')

#Send data in parquet to table in sqls
engine.execute('Delete dbo.Table1')
Data.to_sql('Table1',engine ,if_exists = 'append', index = False)


