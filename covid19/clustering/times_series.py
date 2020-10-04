# clustering/times_series.py

from ..preprocessing.process import Util

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
        data.df["day"] = pd.DatetimeIndex(data.df["Date"]).day
        data.df["month"] = pd.DatetimeIndex(data.df["Date"]).month
        data.delete_nan()
        # data.plot_seasonality_case()
        # data.plot_seasonality_death()
        data.plot_seasonality()
