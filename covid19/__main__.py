# __main__.py

from.preprocessing.EDA import Plot
from .clustering.unsupervised import MyDBSCAN

if __name__ == "__main__":
    Plot.run()
    MyDBSCAN.run()
