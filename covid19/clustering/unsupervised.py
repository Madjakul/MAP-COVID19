# clustering/hierarchical.py

from ..preprocessing.process import Util
from ..preprocessing.feature_extraction import MyPCA, T_SNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import iplot

def label_country(row):
        if row["Fatality_Rate"] < 5:
            return 1
        if row["Fatality_Rate"] >= 5 and row["Fatality_Rate"] < 10:
            return 2
        else:
            return 3


class MyDBSCAN(Util):
    def __init__(self, dataset):
        super().__init__(dataset, dataFrame=True, zip=zip)
        self.clustering = DBSCAN(eps=1, min_samples=10).fit(dataset)

    def get_labels(self):
        self.df["labels"] = self.clustering.labels_
        print(self.clustering.labels_)

    @staticmethod
    def run():
        data = Util("assets/final.csv.gz", zip="gzip")
        data.delete_columns(["Pays_Ou_Entites", "Date", "alpha-3", "Continent", "Sous_Continent", "Superficie_(En_Milliers_De_Km2)",
                                "Population_Mi-2019_(En_Millions)", "Projection_De_La_Population_En_2050_(En_Millions)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)_3",
                                "Taux_de_natalite_(en_%)", "Taux_de_mortalite(en_%)", "Taux_de_mortalite_infantile_(en_%)"])
        data.aggregate_sum(["Country/Region"], True)
        data.delete_columns("Unnamed: 0")
        data.df["Fatality_Rate"] = (data.df["Total_deces"] / data.df["Total_cas_confirmés"]) * 100
        # dataPrincipal = MyPCA(data.df, 3, dataFrame=True)
        data.df["value"] = data.df.apply(lambda row: label_country(row), axis=1)
        data.df = data.df.astype({"value": int})
        dataTSNE = T_SNE(data.df, dataFrame=True)
        dataReduced = dataTSNE.df[['tsne-2d-one', 'tsne-2d-two']].copy()
        cluster = MyDBSCAN(dataReduced)
        cluster.get_labels()
        print(cluster)
        
        data = dict(type = 'choropleth', 
           locations = cluster.df['Country/Region'],
           locationmode = 'country names',
           z = cluster.df['labels'], 
           text = cluster.df['Country/Region'],
           colorbar = {'title':'groupe'})
        layout = dict(title = 'Covid19 fatality rate', 
                    geo = dict(showframe = False, 
                            projection = {'type': 'Mercator'}))
        choromap3 = go.Figure(data = [data], layout=layout)
        iplot(choromap3)

