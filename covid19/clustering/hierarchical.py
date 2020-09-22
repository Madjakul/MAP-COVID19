# clustering/hierarchical.py

from ..preprocessing.process import Util
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
        data.delete_columns(["Country/Region", "Date", "alpha-3", "Continent", "Sous_Continent", "Superficie_(En_Milliers_De_Km2)",
                            "Population_Mi-2019_(En_Millions)", "Projection_De_La_Population_En_2050_(En_Millions)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)_3",
                            "Taux_de_natalite_(en_%)", "Taux_de_mortalite(en_%)", "Taux_de_mortalite_infantile_(en_%)"])
        data.aggregate_sum(["Pays_Ou_Entites"], toSum={"Total_cas_confirmés":"sum", "Total_deces":"sum", "Total_cas_remission":"sum"})
        
        pca = PCA(n_components=2)
        dataPrincipal = pca.fit_transform(data.df)
        dataPrincipal = pd.DataFrame(dataPrincipal)
        dataPrincipal.columns = ['P1', 'P2']

        plt.figure(figsize =(8, 8)) 
        plt.title('Visualising the data') 
        Dendrogram = shc.dendrogram((shc.linkage(dataPrincipal, method ='ward')))
        plt.show()
