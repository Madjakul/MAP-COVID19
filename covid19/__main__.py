# __main__.py

import pandas as pd
from .preprocessing.process import Util
from .elasticsearch.loader import Loader
from .clustering.unsupervised import MyDBSCAN
from .clustering.times_series import TimeSeries, Clustering

if __name__ == "__main__":
    # MyDBSCAN.run()
    # TimeSeries.run()
    Clustering.run()