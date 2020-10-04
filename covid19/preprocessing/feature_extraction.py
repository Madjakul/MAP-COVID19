# preprocessing/feature-extraction.py

from .process import Util

import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import seaborn as sns

from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d
from bokeh.plotting import figure, output_file, show, save


class T_SNE(Util):
    def __init__(self, dataset, excel=False, url=False, dataFrame=False, zip=None):
        super().__init__(dataset, excel=excel, url=url, dataFrame=dataFrame, zip=zip)
        self.tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
        self.tsneResults = self.tsne.fit_transform(self.df)
        self.df["tsne-2d-one"] = self.tsneResults[:, 0]
        self.df["tsne-2d-two"] = self.tsneResults[:, 1]

    def plot(self):
        output_file("assets/t-sne.html", title="Country distribution after t-SNE")
        source = ColumnDataSource(data=self.df.reset_index())
        print(source)
        p = figure(title="Country representation in a two dimensional space after t-SNE")
        p.scatter(x="tsne-2d-one", y="tsne-2d-two", size=8, source=source)
        p.xaxis[0].axis_label = "First dimension"
        p.yaxis[0].axis_label = "Second dimension"
        labels = LabelSet(x="tsne-2d-one", y="tsne-2d-two", text="Country/Region", level='glyph',
                          x_offset=5, y_offset=5, source=source, render_mode="canvas")

        p.add_layout(labels)
        save(p)
        show(p)


class MyPCA(Util):
    def __init__(self, dataset, nComponents, excel=False, url=False, dataFrame=False, zip=None):
        super().__init__(dataset, excel=excel, url=url, dataFrame=dataFrame, zip=zip)
        self.pca = PCA(n_components=nComponents)
        self.pcaResult = self.pca.fit_transform(self.df)
        for i in range(nComponents):
            self.df['pca' + str(i + 1)] = self.pcaResult[:, i]

    def label_point(self, x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            ax.text(point['x']+.02, point['y'], str(point['val']))

    def plot(self):
        output_file("assets/PCA.html", title="Country distribution after PCA")
        source = ColumnDataSource(data=self.df.reset_index())
        print(source)
        p = figure(title="Country representation in a two dimensional space after PCA")
        p.scatter(x="pca1", y="pca2", size=8, source=source)
        p.xaxis[0].axis_label = "First dimension"
        p.yaxis[0].axis_label = "Second dimension"
        labels = LabelSet(x="pca1", y="pca2", text="Country/Region", level='glyph',
                    x_offset=5, y_offset=5, source=source, render_mode="canvas")

        p.add_layout(labels)
        save(p)
        show(p)


    def plot_3d(self, cluster=False):
        ax = plt.figure(figsize=(16,10)).gca(projection='3d')
        ax.scatter(
            xs=self.df["pca1"], 
            ys=self.df["pca2"], 
            zs=self.df["pca3"],
            cmap='tab10'
        )
        ax.set_xlabel('pca-one')
        ax.set_ylabel('pca-two')
        ax.set_zlabel('pca-three')
        plt.savefig("assets/PCA3d.png")
        plt.show()

    def explained_variance(self):
        return self.pca.explained_variance_ratio_
