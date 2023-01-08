import re
import pandas as pd
from conf import OUTPUT_DIR

class parser:

    def __init__(self, text: str):
        self.data = text
        self.result = self.__parse()

    def __parse(self):
        parsed_list = []

        for line in self.data.split('\n'):
            
           if re.match(r"^\d{2}\.\d{2}\.\d{2}\s", line):
        
            transaction = list(filter(None, re.split(r'\s{2,}', line)))
            transaction.insert(2, "NULL") if len(transaction) == 4 else next

            parsed_list.append({
                "DATE": transaction[0],
                "INFO": transaction[1],
                "ACC": transaction[2],
                "AMOUNT": transaction[3],
                "STATE": transaction[4]
            })
        
        df = self.__format(parsed_list)
        df = self.__fix_chars(df)

        return df

    def __format(self, data: list):

        data = pd.DataFrame(data)

        data["DATE"] = pd.to_datetime(data['DATE'], format="%d.%m.%y")

        data["AMOUNT"] = data["AMOUNT"].str.replace(".", "", regex=False)
        data["AMOUNT"] = data["AMOUNT"].str.replace(",", ".", regex=False)
        data["AMOUNT"] = pd.to_numeric(data["AMOUNT"])

        data["STATE"] = data["STATE"].str.replace(".", "", regex=False)
        data["STATE"] = data["STATE"].str.replace(",", ".", regex=False)
        data["STATE"] = pd.to_numeric(data["STATE"])

        return data

    def __fix_chars(self, dataframe: pd.DataFrame()):

        dataframe["INFO"] = dataframe["INFO"].str.replace("‹", "Č", regex=False)
        dataframe["INFO"] = dataframe["INFO"].str.replace("("+"cid:230"+")", "Š", regex=False)
        dataframe["INFO"] = dataframe["INFO"].str.replace("ƒ", "Ž", regex=False)

        return dataframe

    def to_csv(self, name):
        self.result.to_csv(OUTPUT_DIR + name, index=False)
