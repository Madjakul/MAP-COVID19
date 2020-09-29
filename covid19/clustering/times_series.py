# clustering/times_series.py

from ..preprocessing.process import Util

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss, acf, grangercausalitytests
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf,month_plot,quarter_plot
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns

from collections import Counter
import math
import pprint
from datetime import datetime
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster
from scipy import fftpack
from scipy.interpolate import CubicSpline
import time
import json
from fastdtw import fastdtw
import matplotlib.patches as mp

import warnings
warnings.filterwarnings('ignore')


class TimeSeries(Util):
    def __init__(self, dataset, excel=False, url=False, dataFrame=False, zip=None):
        super().__init__(dataset, excel=excel, url=url, dataFrame=dataFrame, zip=zip)

    def plot_death(self):
        fig, ax = plt.subplots(figsize=(15, 6))
        sns.lineplot(self.df["Date"], self.df.groupby("Date", as_index=False).sum()["Total_cas_remission_j"])

        ax.set_title("Nombre de décès journalier", fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax.set_xlabel("Date", fontsize = 16, fontdict=dict(weight='bold'))
        ax.set_ylabel("Nombre de cas confirmé", fontsize = 16, fontdict=dict(weight='bold'))
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=4)
        plt.xticks(rotation=70)
        plt.show()

    def plot_seasonality_case(self):
        fig, ax = plt.subplots(figsize=(15, 6))

        sns.lineplot(self.df["day"], self.df.groupby("Date", as_index=False).sum()["Total_cas_confirmés_j"])
        ax.set_title("Saisonnalité du COVID-19", fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax.set_xlabel("day", fontsize = 16, fontdict=dict(weight='bold'))
        ax.set_ylabel('Nombre de cas confirmés', fontsize = 16, fontdict=dict(weight='bold'))


        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

        sns.boxplot(self.df["month"], self.df.groupby("Date", as_index=False).sum()["Total_cas_confirmés_j"], ax=ax[0])
        ax[0].set_title('Month-wise Box Plot\n(The Trend)', fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax[0].set_xlabel("month", fontsize = 16, fontdict=dict(weight='bold'))
        ax[0].set_ylabel('Nombre de cas confirmés', fontsize = 16, fontdict=dict(weight='bold'))

        sns.boxplot(self.df["day"], self.df.groupby("Date", as_index=False).sum()["Total_cas_confirmés_j"], ax=ax[1])
        ax[1].set_title('Day-wise Box Plot\n(The Seasonality)', fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax[1].set_xlabel("day", fontsize = 16, fontdict=dict(weight='bold'))
        ax[1].set_ylabel('Nombre de cas confirmés', fontsize = 16, fontdict=dict(weight='bold'))

        plt.show()

    def plot_seasonality_death(self):
        fig, ax = plt.subplots(figsize=(15, 6))

        sns.lineplot(self.df["day"], self.df.groupby("Date", as_index=False).sum()["Total_deces_j"])
        ax.set_title("Saisonnalité du nombre de décès dû au COVID-19", fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax.set_xlabel("day", fontsize = 16, fontdict=dict(weight='bold'))
        ax.set_ylabel('Nombre de cas confirmés', fontsize = 16, fontdict=dict(weight='bold'))


        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

        sns.boxplot(self.df["month"], self.df.groupby("Date", as_index=False).sum()["Total_deces_j"], ax=ax[0])
        ax[0].set_title('Month-wise Box Plot\n(The Trend)', fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax[0].set_xlabel("month", fontsize = 16, fontdict=dict(weight='bold'))
        ax[0].set_ylabel('Saisonnalité du nombre de décès dû au COVID-19', fontsize = 16, fontdict=dict(weight='bold'))

        sns.boxplot(self.df["day"], self.df.groupby("Date", as_index=False).sum()["Total_deces_j"], ax=ax[1])
        ax[1].set_title('Day-wise Box Plot\n(The Seasonality)', fontsize = 20, loc='center', fontdict=dict(weight='bold'))
        ax[1].set_xlabel("day", fontsize = 16, fontdict=dict(weight='bold'))
        ax[1].set_ylabel("Saisonnalité du nombre de décès dû au COVID-19", fontsize = 16, fontdict=dict(weight='bold'))

        plt.show()

    def plot_seasonality(self):
        fig, ax = plt.subplots(figsize=(15, 6))

        sns.lineplot(self.df["day"], self.df.groupby("Date", as_index=False).sum()["Total_cas_confirmés_j"], ax=ax)
        ax.set_ylabel('Nombre de cas confirmés')
        ax2 = ax.twinx()
        sns.lineplot(self.df["day"], self.df.groupby("Date", as_index=False).sum()["Total_deces_j"], ax=ax2, color="r")
        ax2.set_ylabel('Nombre de cdécès', color="r")

        plt.show()

    @staticmethod
    def run():
        data = TimeSeries("assets/final.csv.gz", zip="gzip")
        data.delete_columns(["Pays_Ou_Entites", "alpha-3", "Continent", "Sous_Continent", "Superficie_(En_Milliers_De_Km2)",
                            "Population_Mi-2019_(En_Millions)", "Projection_De_La_Population_En_2050_(En_Millions)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)_3",
                            "Taux_de_natalite_(en_%)", "Taux_de_mortalite(en_%)", "Taux_de_mortalite_infantile_(en_%)", "Unnamed: 0"])
        data.df["Total_cas_confirmés_j"] = data.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_cas_confirmés"]
        data.df["Total_deces_j"] = data.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_deces"]
        data.df["Total_cas_remission_j"] = data.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_cas_remission"]
        data.df["day"] = pd.DatetimeIndex(data.df["Date"]).day
        data.df["month"] = pd.DatetimeIndex(data.df["Date"]).month
        data.delete_nan()
        # data.plot_seasonality_case()
        # data.plot_seasonality_death()
        data.plot_seasonality()


class Clustering(Util):
    def __init__(self, dataset, excel=False, url=False, dataFrame=False, zip=None):
        super().__init__(dataset, excel=excel, url=url, dataFrame=dataFrame, zip=zip)

    def ComputeDtw_Matrix(self, mat,window=1): #Apply DTW to matrix. Return dissimilarity matrix
        res=np.zeros((mat.shape[0],mat.shape[0]))
        nb=res.shape[0]
        
        for i in range(nb):
            for j in range(i):
                res[i,j]=fastdtw(mat[i],mat[j],window)[0]
                
        return (res+res.T)

    def ComputeCurveDerivate_Matrix(self, DF):#retourne la derivee des series temporelles
        r,c=DF.shape
        M_derivate=np.zeros((r,len(np.arange(1,c+1))))
        
        for i in range(0,r):
            cs=CubicSpline(np.arange(1,c+1),DF.values[i])
            M_derivate[i]=cs(np.arange(1,c+1),1)#derivee premiere 

        return pd.DataFrame(M_derivate,columns=np.arange(1,c+1),index=DF.index)

    def ComputeDerivativeSpectrum_Matrix(self, DF): #retourne la matrice des spectres
        r,c=DF.shape
        spectre=np.zeros((r,c))
        
        for i,sensor in enumerate(DF.values):
            #Fast Fourier Transfo        
            spectre[i]=abs(np.fft.fft(sensor))
            
        return spectre


    def get_indice_individus(self, clust):#renvoie la position des individus de chaque cluster
        return [list(np.where(clust==elem)[0]) for elem in np.sort(list(Counter(clust)))]

    #def get_individus(clust,data):#renvoie les individus composants chaque cluster
    #    return [data.iloc[list(np.where(clust==elem)[0])].values for elem in np.sort(list(Counter(clust)))]

    def get_individus(self, clust, data):
        dic={}
        for i,classe in enumerate(clust):
            if str(classe) not in dic.keys():
                dic[str(classe)]=[]
            dic[str(classe)].append(data.index[i])

        return (dic)

    def apply_clustering(self, data,k=2,critere="ward",window=1):
        #derivee    
        derivees = self.ComputeCurveDerivate_Matrix(data)

        #Fourier
        spectres = self.ComputeDerivativeSpectrum_Matrix(derivees)

        #DTW
        dist = self.ComputeDtw_Matrix(spectres,window)
        Z=linkage(dist,critere)
        clus=list(fcluster(Z,k,criterion="maxclust"))
        f=fcluster(Z,k,criterion="maxclust")
        
        return clus,Z,f

    @staticmethod
    def run():
        colormap=np.array(['blue','#d10a3c','#6f7bbb','#3ac467','#c69942'])
        data = Clustering("assets/final.csv.gz", zip="gzip")
        data.delete_columns(["Pays_Ou_Entites", "alpha-3", "Continent", "Sous_Continent", "Superficie_(En_Milliers_De_Km2)",
                            "Population_Mi-2019_(En_Millions)", "Projection_De_La_Population_En_2050_(En_Millions)", "Esperance_De_Vie_A_La_Naissance_Hommes_Femmes_(En_Annees)_3",
                            "Taux_de_natalite_(en_%)", "Taux_de_mortalite(en_%)", "Taux_de_mortalite_infantile_(en_%)", "Unnamed: 0"])
        data.df["Total_cas_confirmés"] = data.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_cas_confirmés"]
        data.df["Total_deces"] = data.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_deces"]
        data.df["Total_cas_remission"] = data.df.drop(columns=["Date"], axis=1).groupby("Country/Region", as_index=False).diff()["Total_cas_remission"]
        data.delete_columns(["Date", "Country/Region"])
        data.delete_nan()
        #days k=2
        start=time.time()
        cl2,z2,f2=data.apply_clustering(data.df,k=2,window=2)
        print("temps d'exécution: ",time.time()-start,'s')
        classes=data.get_individus(cl2,data.df)

        #plot
        data.df.T.plot(legend=False,color=colormap[cl2] ,title='Clustering 2 groupes',figsize=(7,4))
        plt.xlabel("Date")
        plt.ylabel("Conso(kwh)")
