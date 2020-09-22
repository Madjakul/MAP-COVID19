from ..preprocessing.process import Util
from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd


class Loader(Util):
    def __init__(self, dataset, zip):
        super().__init__(dataset, zip=zip)

    def to_dict(self, orient):
        self.dict = self.df.to_dict(orient=orient) 

    @staticmethod
    def run():
        es = Elasticsearch()
        myData = Loader("assets/final.csv.gz", "gzip")
        myData.to_dict(orient="records")
        helpers.bulk(es, myData.dict, index="covid19")
        print("Succès !")