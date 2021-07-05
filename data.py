#from polygon_config import POLYGON_API_TOKEN
import json
import quandl
import pandas as pd
import datetime
import numpy as np
from quandl_config import API_KEY

# from polygon_config import POLYGON_API_TOKEN

# The following code uses polygon.io as data source
# Data = f"https://api.polygon.io/v1/open-close/AAPL/2020-10-14?adjusted=true&apiKey={POLYGON_API_TOKEN}"

# data = requests.get(Data)

# print(data.json())
# , start_date="2020-1-1", end_date="2021-1-31"


# The follwing code uses quandl as data source
data = quandl.get(
    "HKEX/00001", authtoken=API_KEY, start_date="2020-1-1", end_date="2021-1-31")


# set datetime as index
df = pd.DataFrame(data)


core_five = df[["High", "Low", "Nominal Price",
                "Previous Close", "Share Volume (000)"]]

ncf = core_five.rename(columns={"Nominal Price": "Close",
                                "Share Volume (000)": "Volume (000)"})


#new_core_five.to_csv('00001.csv', index=False)

# print(new_core_five)
