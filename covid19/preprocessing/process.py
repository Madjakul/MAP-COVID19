# preprocessing/process.py

import pandas as pd
import numpy as np
import pycountry
from .translate import CountryTranslator


class Util:
    '''
    Regroupe toutes les fonctions nécessaire à preprocess et initialiser un dataframe
    '''
    def __init__(self, dataset, excel=False, url=False, dataFrame=False, zip=None):
        if url == False and dataFrame == False:
            if zip is None:
                self.df = pd.read_excel(dataset) if excel else pd.read_csv(dataset, index_col=0)
            else:
                self.df = pd.read_csv(dataset, compression=zip)
        elif dataFrame == True:
            self.df = dataset
        else:
            self.df = pd.read_csv(dataset, error_bad_lines=False)

    def melt(self, newIndexes, varName):
        # Melt et trie les données en fonction du pays et de la date
        self.df = self.df.melt(id_vars=newIndexes, var_name=varName)

    def to_datetime(self, index):
        self.df[index] = pd.to_datetime(self.df[index])

    def sort(self, sortedBy):
        self.df = self.df.sort_values(sortedBy)

    def write(self):
        self.df.to_csv('assets/exit.csv', encoding='utf-8')

    def aggregate_sum(self, id, index=False):
        # Fais la somme de chaque ligne en fonction du pays
        self.df = self.df.groupby(id, as_index=False).sum() if index == False else self.df.groupby(id).sum()

    def rename_column(self, oldName, newName):
        self.df.rename(columns = {oldName:newName}, inplace = True)

    def delete_columns(self, columns):
        self.df.drop(columns=columns, axis=1, inplace=True)

    def delete_duplicate(self, subset=None):
        self.df = self.df.drop_duplicates() if subset is None else self.df.drop_duplicates(subset=subset)

    def reset_index(self):
        self.df = self.df.reset_index()

    def to_csv(self, name, encoding):
        self.df.to_csv(name, encoding=encoding)
    
    def translate_countries(self, column):
        countryList = []
        for country in self.df[column]:
            translator = CountryTranslator()
            [countryList.append(i) for i in translator.translate(country)]
        self.df["Country_FR"] = countryList

    def create_primary_key(self, column1, column2):
        # Combine deux labels afin de créer une clé primaire pour un dataframe
        self.df["Primary_Key"] = self.df[column1].astype(str) + self.df[column2].astype(str)

    def __add__(self, other):
        return Util(pd.merge(self.df, other.df), dataFrame=True)

    def __str__(self):
        return (str(self.df.info()) + "\n" + str(self.df))

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
        covidDf.reset_index()
        covidDf.delete_columns(["Num_ligne", "Id", "Total_cas_confirmes", "Total_deces", "Total_cas_remission", "Date"])
        covidDf.delete_duplicate(subset=["Pays_Ou_Entites"])

        thirdMerge = secondMerge + covidDf

        hopkinsDf3 = Util("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv", url=True) # Données sur le nombre de guérison
        hopkinsDf3.aggregate_sum("Country/Region")
        hopkinsDf3.delete_columns(["Lat", "Long"])
        hopkinsDf3.melt(["Country/Region"], "Date") # Transforme les colonnes en ligne, le tout par pays
        hopkinsDf3.to_datetime("Date") # Transforme la colonne date du dataframe en datetime64
        hopkinsDf3.rename_column("value", "Total_cas_remission")

        lastMerge = thirdMerge + hopkinsDf3
        lastMerge.df.to_csv("assets/final.csv.gz", compression="gzip", encoding="utf-8")
