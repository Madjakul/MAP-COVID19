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

    def rename_column(self, oldName, newName):
        self.df.rename(columns = {oldName:newName}, inplace = True)

    def delete_columns(self, columns):
        self.df.drop(columns, axis=1, inplace=True)
    
    def translate_countries(self, column):
        countryList = []
        for country in self.df[column]:
            translator = CountryTranslator()
            [countryList.append(i) for i in translator.translate(country)]
        self.df["Country_FR"] = countryList

    def get_alpha2(self):
        pass

    def __str__(self):
        return (str(self.df.info()) + "\n" + str(self.df))
