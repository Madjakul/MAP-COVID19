import pandas as pd
from .process import Util


class Merge():
    # Ne peut merge que deux datasets
    def __init__(self, datasets):
        pass

    @staticmethod
    def run():
        hopkinsDf = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", url=True) # DOnnées sur le nombre de cas confirnmés par pays
        hopkinsDf.df["Country/Region"].replace("US", "United States", inplace=True)
        hopkinsDf.aggregate_sum("Country/Region")
        hopkinsDf.delete_columns(["Lat", "Long"])
        hopkinsDf.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf.sort(["Country/Region", "Date"]) # classe le dataframe par pays et par date
        hopkinsDf.rename_column("Country/Region", "Country_Region")
        hopkinsDf.rename_column("value", "Total_cas_confirmés")
        hopkinsDf.translate_countries("Country_Region") # Traduit le pays de l'anglais au français
        hopkinsDf.create_primary_key("Country_FR", "Date") #Crée une clé primaire artificielle à partire des deux colonnes citées

        hopkinsDf2 = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv", url=True) # Données sur le nombre de morts
        hopkinsDf2.df["Country/Region"].replace("US", "United States", inplace=True)
        hopkinsDf2.aggregate_sum("Country/Region")
        hopkinsDf2.delete_columns(["Lat", "Long"])
        hopkinsDf2.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf2.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf2.sort(["Country/Region", "Date"]) # classe le dataframe par pays et par date
        hopkinsDf2.rename_column("Country/Region", "Country_Region")
        hopkinsDf2.rename_column("value", "Total_deces")
        hopkinsDf2.translate_countries("Country_Region") # Traduit le pays de l'anglais au français
        hopkinsDf2.create_primary_key("Country_FR", "Date") #Crée une clé primaire artificielle à partire des deux colonnes citées
        hopkinsDf2.delete_columns(["Country_FR", "Date"])

        covidDf = Util("assets/df_covid_20aug.csv")
        covidDf.delete_columns(["Num_ligne", "Id", "Total_cas_confirmés", "Total_deces", "Total_cas_remission"])
        covidDf.to_datetime("Date")
        covidDf.sort(["Pays_Ou_Entités", "Date"])
        covidDf.create_primary_key("Pays_Ou_Entités", "Date")
        covidDf.delete_columns(["Pays_Ou_Entités"])

        mergedDf = hopkinsDf + covidDf # Merge les deux bases de données en fonction d'une clé primaire

        hopkinsDf3 = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv", url=True) # Données sur le nombre de guérison
        hopkinsDf3.df["Country/Region"].replace("US", "United States", inplace=True)
        hopkinsDf3.aggregate_sum("Country/Region")
        hopkinsDf3.delete_columns(["Lat", "Long"])
        hopkinsDf3.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf3.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf3.sort(["Country/Region", "Date"]) # classe le dataframe par pays et par date
        hopkinsDf3.rename_column("Country/Region", "Country_Region")
        hopkinsDf3.rename_column("value", "Total_cas_remission")
        hopkinsDf3.translate_countries("Country_Region") # Traduit le pays de l'anglais au français
        hopkinsDf3.create_primary_key("Country_FR", "Date") #Crée une clé primaire artificielle à partire des deux colonnes citées
        hopkinsDf3.delete_columns(["Country_FR", "Date"])

        tempDf = pd.merge(hopkinsDf2.df, mergedDf)
        finalDf = pd.merge(hopkinsDf3.df, tempDf)
        finalDf.rename(columns = {"Country_Region":"Pays_Ou_Entités"}, inplace = True)
        finalDf.rename(columns = {"Country_FR":"Pays_Ou_Entités_TRAD"}, inplace = True)
        finalDf["Location"] = finalDf["Lat"].astype(str) +", " +  finalDf["Long"].astype(str)
        finalDf.to_csv("assets/final.csv", encoding="utf-8")
