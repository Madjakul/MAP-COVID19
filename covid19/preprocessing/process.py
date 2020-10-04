# preprocessing/process.py

import pandas as pd
import numpy as np


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

    def aggregate(self, id, items, newItems):
        # Fais la somme de chaque ligne en fonction du pays
        self.df = self.df.groupby(id).agg(items)
        self.df.columns = newItems
        self.df = self.df.reset_index()

    def aggregate_sum(self, id):
        self.df = self.df.groupby(id, as_index=False).sum()

    def rename_column(self, oldName, newName):
        self.df.rename(columns = {oldName:newName}, inplace = True)

    def delete_columns(self, columns):
        self.df.drop(columns=columns, axis=1, inplace=True)

    def delete_nan(self):
        self.df = self.df.dropna()

    def delete_duplicate(self, subset=None):
        self.df = self.df.drop_duplicates() if subset is None else self.df.drop_duplicates(subset=subset)

    def reset_index(self):
        self.df = self.df.reset_index()
    
    def set_index(self, id):
        self.df = self.df.set_index(id)

    def to_csv(self, name, encoding):
        self.df.to_csv(name, encoding=encoding)

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
        # here we remove the useless data
        lastMerge.delete_columns(["Pays_Ou_Entites", "alpha-3", "Continent", "Sous_Continent", "Superficie_(En_Milliers_De_Km2)",
                                "Population_Mi-2019_(En_Millions)", "Projection_De_La_Population_En_2050_(En_Millions)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)_3",
                                "Taux_de_natalite_(en_%)", "Taux_de_mortalite(en_%)", "Taux_de_mortalite_infantile_(en_%)", "Population_de_moins_de_15_ans", "Population_de_65_ans_ou_plus"])
        # The data is cumulative, which cause some problem later on the project, let's retrive the daily reports from Hopkins cumuutaive data
        lastMerge.df["Total_cas_confirmés"] = lastMerge.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_cas_confirmés"]
        lastMerge.df["Total_deces"] = lastMerge.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_deces"]
        lastMerge.df["Total_cas_remission"] = lastMerge.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_cas_remission"]
        lastMerge.delete_nan()
        lastMerge.df.to_csv("assets/final.csv.gz", compression="gzip", encoding="utf-8")
