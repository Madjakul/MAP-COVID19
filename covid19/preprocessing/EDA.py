# preprocessing/EDA.py

from .process import Util
from .feature_extraction import MyPCA, T_SNE


class Plot(Util):
    """
    This class is only used for Exploratory Data Analysis by reducing dimensionality ploting scatterplot to have an intuition about the data
    """
    def __init__(self, dataset):
        super().__init__(dataset, dataFrame=True, zip=zip)
    
    @staticmethod
    def run():
        data = Util("assets/final.csv.gz", zip="gzip")
        data.delete_columns(["Date", "Lat", "Long"])
        data.aggregate(["Country/Region", "Superficie_(En_Km2)", "Population_Mi-2019", "Taux_De_Natalite_(Pour_1_000_Habitants)", "Taux_De_Mortalite_(Pour_1_000_Habitants)", "Projection_De_La_Population_En_2050", "Taux_De_Mortalite_Infantile_(Pour_1_000_Naissances)", "Indice_Synthetique_De_Fecondite_(Enfants_Par_Femme)", "Proportion_De_Moins_De_15_Ans_(En_%)", "Proportion_De_65_Ans_Ou_Plus_(En_%)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)", "Revenu_National_Brut_P.P.A._Par_Hab._En_2018_(En_Dollars_Us)"],
                            {"Total_cas_confirmés": ["sum"], "Total_deces": ["sum"], "Total_cas_remission": ["sum"]},
                            ["Total_cas_confirmés", "Total_deces" ,"Total_cas_remission"])
        data.set_index("Country/Region")
        
        dataTSNE = T_SNE(data.df, dataFrame=True)
        dataTSNE.plot()
        dataPrincipal = MyPCA(data.df, 3, dataFrame=True)
        dataPrincipal.plot()
        dataPrincipal.plot_3d()