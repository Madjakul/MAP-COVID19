from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd


class Loader():
    def __init__(self):
        pass

    @staticmethod
    def run():
        es = Elasticsearch()
        myData = pd.read_csv("assets/final.csv.gz", compression="gzip")
        documents = myData.to_dict(orient="records")
        helpers.bulk(es, documents, index="covid19")
        print("Succès !")