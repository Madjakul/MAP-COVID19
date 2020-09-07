import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("assets/time_series_covid19_confirmed_global.csv")
    print(df)
    print("preprocessing")
    df = df.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], var_name="Date")
    print(df)
    print("Result after sorting")
    df = df.sort_values(by ="Country/Region")
    print(df)
