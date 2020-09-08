import pandas as pd
import numpy as np
import re

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
        self.df.to_csv('assets/file_name.csv', encoding='utf-8')

    def delete_columns(self, columns):
        self.df.drop(columns, axis=1, inplace=True)

    def __str__(self):
        return (str(self.df.info()) + "\n" + str(self.df))
