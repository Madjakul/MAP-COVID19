# __main__.py

import pandas as pd
from .preprocessing.process import Util
from .elasticsearch.loader import Loader
from .clustering.hierarchical import SL

if __name__ == "__main__":
    SL.run()
