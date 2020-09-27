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
            # hue="Pays_Ou_Entites",
            palette=sns.color_palette("hls", 10),
            data=self.df,
            legend="full",
            alpha=0.3
        )
        plt.show()

    def explained_variance(self):
        return self.pca.explained_variance_ratio_