import pandas as pd
from .process import Util

class Merge():
    # Ne peut merge que deux datasets
    def __init__(self, datasets):
        self.database = datasets

    @staticmethod
    def run():
        hopkinsDf = Util("assets/time_series_covid19_confirmed_global.csv")
        hopkinsDf.delete_columns(["Province/State"])
        hopkinsDf.melt(["Country/Region", "Lat", "Long"], "Date")
        hopkinsDf.to_datetime("Date")
        hopkinsDf.sort(["Country/Region", "Date"])
        print(hopkinsDf)

        covidDf = Util("assets/df_covid_20aug.csv")
        covidDf.delete_columns(["Num_ligne", "Id"])
        covidDf.to_datetime("Date")
        covidDf.sort(["Pays_Ou_Entites", "Date"])
        print(covidDf)

        db = Merge((hopkinsDf, covidDf))
