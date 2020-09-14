import pandas as pd
import numpy as np
import pycountry
from .translate import CountryTranslator


class Util:
    def __init__(self, dataset, excel=False):
        self.df = pd.read_excel(dataset) if excel else pd.read_csv(dataset)

    def melt(self, newIndexes, varName):
        # Melt et trie les données en fonction du pays et de la date
        self.df = self.df.melt(id_vars=newIndexes, var_name=varName)

    def to_datetime(self, index):
        self.df[index] = pd.to_datetime(self.df[index])

    def sort(self, sortedBy):
        self.df = self.df.sort_values(sortedBy)

    def write(self):
        self.df.to_csv('assets/exit.csv', encoding='utf-8')

    def aggregate_sum(self, id):
        # Fais la somme de chaque ligne en fonction du pays
        self.df = self.df.groupby(id, as_index=False).sum()

    def rename_column(self, oldName, newName):
        self.df.rename(columns = {oldName:newName}, inplace = True)

    def delete_columns(self, columns):
        self.df.drop(columns=columns, axis=1, inplace=True)
    
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
        return pd.merge(self.df, other.df)

    def __str__(self):
        return (str(self.df.info()) + "\n" + str(self.df))
