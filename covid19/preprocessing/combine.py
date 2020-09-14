import pandas as pd
from .process import Util


class Merge():
    # Ne peut merge que deux datasets
    def __init__(self, datasets):
        self.database = datasets

    @staticmethod
    def run():
        hopkinsDf = Util("assets/time_series_covid19_confirmed_global.csv")
        hopkinsDf.df["Country/Region"].replace("US", "United States", inplace=True)
        hopkinsDf.df.to_csv('assets/test.csv', encoding='utf-8')
        hopkinsDf.aggregate_sum("Country/Region")
        hopkinsDf.delete_columns(["Lat", "Long"])
        hopkinsDf.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf.sort(["Country/Region", "Date"]) # classe le dataframe par pays et par date
        hopkinsDf.rename_column("Country/Region", "Country_Region")
        hopkinsDf.translate_countries("Country_Region") # Traduit le pays de l'anglais au français
        hopkinsDf.create_primary_key("Country_FR", "Date") #Crée une clé primaire artificielle à partire des deux colonnes citées

        covidDf = Util("assets/df_covid_20aug.csv")
        covidDf.delete_columns(["Num_ligne", "Id"])
        covidDf.to_datetime("Date")
        covidDf.sort(["Pays_Ou_Entités", "Date"])
        covidDf.create_primary_key("Pays_Ou_Entités", "Date")

        mergedDf = hopkinsDf + covidDf # Merge les deux bases de données en fonction d'une clé primaire
        mergedDf.drop(columns=["Pays_Ou_Entités"], axis=1, inplace=True)
        mergedDf.rename(columns = {"value":"Total_cas_confirmés_EN"}, inplace = True)
        mergedDf.rename(columns = {"Country_Region":"Pays_Ou_Entités_EN"}, inplace = True)
        mergedDf.rename(columns = {"Country_FR":"Pays_Ou_Entités_TRAD"}, inplace = True)
        mergedDf.to_csv('assets/exit.csv', encoding='utf-8')
