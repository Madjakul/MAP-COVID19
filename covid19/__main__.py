import pandas as pd
from .preprocessing.combine import Merge
from .elasticsearch.loader import Loader

if __name__ == "__main__":
    Merge.run()
    Loader.run()
