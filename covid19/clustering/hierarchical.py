# clustering/hierarchical.py

from ..preprocessing.process import Util
from ..preprocessing.feature_extraction import MyPCA
from sklearn.decomposition import PCA 
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
import pandas as pd


class SL(Util):
    def __init__(self, dataset, zip):
        super().__init__(dataset, zip=zip)

    @staticmethod
    def run():
        data = SL("assets/final.csv.gz", "gzip")
        print("preprocess")
        data.delete_columns(["Country/Region", "Date", "alpha-3", "Continent", "Sous_Continent", "Superficie_(En_Milliers_De_Km2)",
                            "Population_Mi-2019_(En_Millions)", "Projection_De_La_Population_En_2050_(En_Millions)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)_3",
                            "Taux_de_natalite_(en_%)", "Taux_de_mortalite(en_%)", "Taux_de_mortalite_infantile_(en_%)"])
        data.aggregate_sum(["Pays_Ou_Entites"], True)
        data.delete_columns("Unnamed: 0")
        """
        pca = PCA(n_components=2)
        dataPrincipal = pca.fit_transform(data.df)
        dataPrincipal = pd.DataFrame(dataPrincipal)
        dataPrincipal.columns = ['P1', 'P2']
        """
        """
        plt.figure(figsize =(8, 8)) 
        plt.title('Visualising the data') 
        Dendrogram = shc.dendrogram((shc.linkage(dataPrincipal, method ='ward')))
        plt.show()
        """
        """
        labels = data.df.index
        plt.figure(figsize=(10, 7))
        plt.subplots_adjust(bottom=0.1)
        plt.scatter(dataPrincipal["P1"],dataPrincipal["P2"], label='True Position')

        for label, x, y in zip(labels, dataPrincipal["P1"], dataPrincipal["P2"]):
            plt.annotate(
                label,
                xy=(x, y), xytext=(-3, 3),
                textcoords='offset points', ha='right', va='bottom')
        plt.show()
        """
        dataPrincipal = MyPCA(data.df, 3, dataFrame=True)
        print(dataPrincipal.explained_variance())
        dataPrincipal.plot()
