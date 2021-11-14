import sqlite3
import os

import pandas as pd

DATAFOLDER = 'ETHBTC'
TABLE = 'KLINES_15M'

conn = sqlite3.connect('kline_data.db')

print("Opened database successfully")

# Schauen ob Tabelle existiert
c = conn.cursor()
c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{TABLE}';")

if c.fetchone()[0] == 1:
    print('Table exists.')
else:
    conn.execute(f"CREATE TABLE {TABLE}" +
                 "(ID                INTEGER PRIMARY KEY AUTOINCREMENT, " +
                 "SYMBOL             TEXT            NOT NULL, " +
                 "OPENTIME           TEXT            NOT NULL, " +
                 "OPEN               REAL            NOT NULL, " +
                 "HIGH               REAL, " +
                 "LOW                REAL, " +
                 "CLOSE              REAL, " +
                 "VOLUME             REAL, " +
                 "CLOSETIME          REAL, " +
                 "QUOTEASSETVOL      REAL, " +
                 "NumOfTrades        REAL, " +
                 "TakeBaseVolume     REAL, " +
                 "TakeQuoteVolume    REAL, " +
                 "IGNORE             REAL);")

# Browse den Baseordner nach dateien
files = os.listdir(DATAFOLDER)
counter = 0
for file in files:
    df = pd.read_csv(DATAFOLDER + "/" + file)
    for index, data in df.iterrows():
        query = f"INSERT INTO {TABLE} (SYMBOL,OPENTIME,OPEN,HIGH,LOW,CLOSE,VOLUME,CLOSETIME,QUOTEASSETVOL,NumOfTrades,\
                        TakeBaseVolume,TakeQuoteVolume,IGNORE) \n\
                        values ('{DATAFOLDER}',{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]},{data[7]},{data[8]},{data[9]},{data[10]},\
                        {data[11]});"
        conn.execute(query)
        counter = counter + 1
    conn.commit()
print(f"es wurden {counter} datensätze erfolgreich hinzugefügt")
