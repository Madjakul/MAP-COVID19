import pandas as pd
from .process import Util


class Merge(Util):
    # Ne peut merge que deux datasets
    def __init__(self, dataset):
        super().__init__(self, dataset, dataFrame=True)

    @staticmethod
    def run():
        countryTable = Util("assets/sql-paysC.csv")
        countryTable.delete_columns(["Num", "alpha-2"])

        hopkinsDf = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", url=True) # DOnnées sur le nombre de cas confirnmés par pays
        hopkinsDf.aggregate_sum("Country/Region")
        hopkinsDf.delete_columns(["Lat", "Long"])
        hopkinsDf.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf.rename_column("value", "Total_cas_confirmés")

        firstMerge = hopkinsDf + countryTable

        hopkinsDf2 = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv", url=True) # Données sur le nombre de morts
        hopkinsDf2.aggregate_sum("Country/Region")
        hopkinsDf2.delete_columns(["Lat", "Long"])
        hopkinsDf2.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf2.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf2.rename_column("value", "Total_deces")

        secondMerge = firstMerge + hopkinsDf2

        covidDf = Util("assets/df_covid_20aug.csv")
        covidDf.delete_columns(["Id", "Total_cas_confirmes", "Total_deces", "Total_cas_remission"])
        covidDf.to_datetime("Date")

        thirdMerge = secondMerge + covidDf

        hopkinsDf3 = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv", url=True) # Données sur le nombre de guérison
        hopkinsDf3.aggregate_sum("Country/Region")
        hopkinsDf3.delete_columns(["Lat", "Long"])
        hopkinsDf3.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf3.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf3.rename_column("value", "Total_cas_remission")

        lastMerge = thirdMerge + hopkinsDf3

        lastMerge.df.to_csv("assets/final.csv.gz", compression="gzip", encoding="utf-8")