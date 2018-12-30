import json
import pandas
import urllib
import urllib.request
import os
import gzip
from db.postgresDumpParser import PostgresDumpParser as dcp



url = "http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz"
file_folder = "D:\Anna_Breit\master_thesis\playground"
file_name = "sql_dump.sql.gz"
file = os.path.join(file_folder, file_name)

urllib.request.urlretrieve(url, file)

df = dcp.table_to_df(file, "omop_relationship")
print(df)