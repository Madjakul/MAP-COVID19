# clustering/hierarchical.py

from ..preprocessing.process import Util
from ..preprocessing.feature_extraction import MyPCA, T_SNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

import plotly.graph_objs as go
from plotly.offline import iplot


class MyDBSCAN(Util):
    def __init__(self, dataset):
        super().__init__(dataset, dataFrame=True, zip=zip)
        self.clustering = DBSCAN(eps=1, min_samples=10).fit(dataset)

    def get_labels(self):
        self.df["labels"] = self.clustering.labels_

    def plot(self):
        self.get_labels()
        self.reset_index()
        data = dict(type = 'choropleth', 
           locations = self.df['Country/Region'],
           locationmode = 'country names',
           z = self.df['labels'], 
           text = self.df['Country/Region'],
           colorbar = {'title':'groupe'})
        layout = dict(title = 'Country clustering after t-SNE', 
                    geo = dict(showframe = False, 
                            projection = {'type': 'mercator'}))
        choromap3 = go.Figure(data = [data], layout=layout)
        with open("assets/choromap.html", "w") as f:
            f.write(choromap3.to_html(include_plotlyjs="cdn"))
        choromap3.show()


    @staticmethod
    def run():
        data = Util("assets/final.csv.gz", zip="gzip")
        data.delete_columns(["Date", "Lat", "Long"])
        data.aggregate(["Country/Region", "Superficie_(En_Km2)", "Population_Mi-2019", "Taux_De_Natalite_(Pour_1_000_Habitants)", "Taux_De_Mortalite_(Pour_1_000_Habitants)", "Projection_De_La_Population_En_2050", "Taux_De_Mortalite_Infantile_(Pour_1_000_Naissances)", "Indice_Synthetique_De_Fecondite_(Enfants_Par_Femme)", "Proportion_De_Moins_De_15_Ans_(En_%)", "Proportion_De_65_Ans_Ou_Plus_(En_%)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)", "Revenu_National_Brut_P.P.A._Par_Hab._En_2018_(En_Dollars_Us)"],
                            {"Total_cas_confirmés": ["sum"], "Total_deces": ["sum"], "Total_cas_remission": ["sum"]},
                            ["Total_cas_confirmés", "Total_deces" ,"Total_cas_remission"])
        data.set_index("Country/Region")
        dataTSNE = T_SNE(data.df, dataFrame=True)
        dataPrincipal = MyPCA(data.df, 3, dataFrame=True)
        print(dataPrincipal.explained_variance())
        
        dataReduced = dataTSNE.df[['tsne-2d-one', 'tsne-2d-two']].copy()
        cluster = MyDBSCAN(dataReduced)
        cluster.plot()
