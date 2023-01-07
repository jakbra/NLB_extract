import re
from pdfminer.high_level import extract_text
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

text = extract_text("./sample.pdf")

df = []

for line in text.split('\n'):

    if re.match(r"^\d{2}\.\d{2}\.\d{2}\s", line):
        
        transaction = list(filter(None, re.split(r'\s{2,}', line)))

        transaction.insert(2, "NULL") if len(transaction) == 4 else next

        df.append({
            "DATE": transaction[0],
            "INFO": transaction[1],
            "ACC": transaction[2],
            "AMOUNT": transaction[3],
            "STATE": transaction[4]
        })


df = pd.DataFrame(df)

df["DATE"] = pd.to_datetime(df['DATE'], format="%d.%m.%y")

df["AMOUNT"] = df["AMOUNT"].str.replace(".", "", regex=False)
df["AMOUNT"] = df["AMOUNT"].str.replace(",", ".", regex=False)
df["AMOUNT"] = pd.to_numeric(df["AMOUNT"])

df["STATE"] = df["STATE"].str.replace(".", "", regex=False)
df["STATE"] = df["STATE"].str.replace(",", ".", regex=False)
df["STATE"] = pd.to_numeric(df["STATE"])

df["INFO"] = df["INFO"].str.replace("‹", "Č", regex=False)
df["INFO"] = df["INFO"].str.replace("("+"cid:230"+")", "Š", regex=False)
df["INFO"] = df["INFO"].str.replace("ƒ", "Ž", regex=False)

print(df)