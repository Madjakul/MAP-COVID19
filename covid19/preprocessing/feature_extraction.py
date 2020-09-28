# preprocessing/feature-extraction.py

from .process import Util

import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import seaborn as sns


class T_SNE(Util):
    def __init__(self, dataset, excel=False, url=False, dataFrame=False, zip=None):
        super().__init__(dataset, excel=excel, url=url, dataFrame=dataFrame, zip=zip)
        self.tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
        self.tsneResults = self.tsne.fit_transform(self.df[["value"]].values)
        self.df['tsne-2d-one'] = self.tsneResults[:,0]
        self.df['tsne-2d-two'] = self.tsneResults[:,1]

    def plot(self):
        plt.figure(figsize=(16,10))
        sns.scatterplot(
            x="tsne-2d-one", y="tsne-2d-two",
            hue=self.df.value.tolist(),
            palette=sns.color_palette("hls", 3),
            data=self.df,
            legend="full",
            alpha=0.3
        )
        plt.show()


class MyPCA(Util):
    def __init__(self, dataset, nComponents, excel=False, url=False, dataFrame=False, zip=None):
        super().__init__(dataset, excel=excel, url=url, dataFrame=dataFrame, zip=zip)
        self.pca = PCA(n_components=nComponents)
        self.pcaResult = self.pca.fit_transform(self.df)
        for i in range(nComponents):
            self.df['pca'+str(i+1)] = self.pcaResult[:,i]
    
    def plot(self):
        plt.figure(figsize=(16,10))
        sns.scatterplot(
            x="pca1", y="pca2",
            hue=self.df.value.tolist(),
            palette=sns.color_palette("hls", 3),
            data=self.df,
            alpha=0.3
        )
        plt.show()

    def plot_3d(self):
        ax = plt.figure(figsize=(16,10)).gca(projection='3d')
        ax.scatter(
            xs=self.df["pca1"], 
            ys=self.df["pca2"], 
            zs=self.df["pca3"], 
            c=self.df["value"], 
            cmap='tab10'
        )
        ax.set_xlabel('pca-one')
        ax.set_ylabel('pca-two')
        ax.set_zlabel('pca-three')
        plt.show()

    def explained_variance(self):
        return self.pca.explained_variance_ratio_