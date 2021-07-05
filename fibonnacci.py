# import libraries
# from polygon_config import POLYGON_API_TOKEN
import json
from pandas.core.indexes.base import Index
import quandl
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from quandl_config import API_KEY
plt.style.use('fivethirtyeight')

# from polygon_config import POLYGON_API_TOKEN

# The following code uses polygon.io as data source
# Data = f"https://api.polygon.io/v1/open-close/AAPL/2020-10-14?adjusted=true&apiKey={POLYGON_API_TOKEN}"

# data = requests.get(Data)

# print(data.json())
# , start_date="2020-1-1", end_date="2021-1-31"


# The follwing code uses quandl as data source
data = quandl.get(
    "HKEX/09988", authtoken=API_KEY, start_date="2019-1-1", end_date="2021-3-31")


# set datetime as index
df = pd.DataFrame(data)


core_five = df[["High", "Low", "Nominal Price",
                "Previous Close", "Share Volume (000)"]]

ncf = core_five.rename(columns={"Nominal Price": "Close",
                                "Share Volume (000)": "Volume (000)"})


# Calcualte the Fibonacci Retractment levels

max_price = ncf['Close'].max()
min_price = ncf['Close'].min()

difference = max_price - min_price
first_level = max_price - difference * 0.236
second_level = max_price - difference * 0.382
third_level = max_price - difference * 0.5
fourth_level = max_price - difference * 0.618

# Calculate the MACD line and the Signal Line indicator
# Calculate the Short Term exponention Moving Average

ShortEMA = ncf.Close.ewm(span=12, adjust=False).mean()
# Calcualte the Long term Exponentila Moving Average

LongEMA = ncf.Close.ewm(span=26, adjust=False).mean()

# Cacualte the Moving Average Convergence/Divergence (MACD)
MACD = ShortEMA - LongEMA

# Calcualte the Signal Line
signal = MACD.ewm(span=9, adjust=False).mean()

# Plot the fibonacci Levels along with the close price and the MACD and signal line
new_df = ncf


# plot the Fibonacci Levels
# plt.figure(figsize=(12.33, 9.5))
# plt.subplot(2, 1, 1)
# plt.plot(new_df.index, new_df['Close'])
# plt.axhline(max_price, linestyle='--', alpha=0.5, color='red')
# plt.axhline(first_level, linestyle='--', alpha=0.5, color='orange')
# plt.axhline(second_level, linestyle='--', alpha=0.5, color='yellow')
# plt.axhline(third_level, linestyle='--', alpha=0.5, color='green')
# plt.axhline(fourth_level, linestyle='--', alpha=0.5, color='blue')
# plt.axhline(min_price, linestyle='--', alpha=0.5, color='purple')
# plt.ylabel('Fibonacci')

# Plot the MACD Line and the Signal Line

# plt.subplot(2, 1, 2)
# plt.plot(new_df.index, MACD)
# plt.plot(new_df.index, signal)
# plt.ylabel('MACD')
# plt.xticks(rotation=45)
# plt.show()

# Create new columns for the data frame
ncf['MACD'] = MACD
ncf['Signal Line'] = signal


# Create a function to be used in our strategy to get the upeer fibonacci level and the lower fibonacci level of the current price

def getlevels(price):
    if price >= first_level:
        return (max_price, first_level)
    elif price >= second_level:
        return(first_level, second_level)
    elif price >= third_level:
        return(second_level, third_level)
    elif price >= fourth_level:
        return(third_level, fourth_level)
    else:
        return(fourth_level, min_price)

# Create a function for the trading strategy

# The strategy

# If the signal leine crosses above the MACD line and the current price crossed above ot below the last Fibonacci level, then buy

# If the signal line crosses below the MACD Line and the current price corssed above or below the last Fibonacci level , then sell

# Never sell at a price that is lower than I bought


def strategy(df):
    buy_list = []
    sell_list = []
    flag = 0
    last_buy_price = 0

    # Loop through the data set
    for i in range(0, df.shape[0]):
        price = ncf['Close'][i]
        # If this is the first data point within the data set, then get the elvel above and below it
        if i == 0:
            upper_lvl, lower_lvl = getlevels(price)
            buy_list.append(np.nan)
            sell_list.append(np.nan)
        # Else if the current price is gretaer than or equal to the upper level ot less than ot equal to the lower level, then we knoe the price has 'hit' or crossed a fibonacci level
        elif price >= upper_lvl or price <= lower_lvl:

            # Check to see if the MACD line crossed above or below the signal line
            if ncf['Signal Line'][i] > ncf['MACD'][i] and flag == 0:
                last_buy_price = price
                buy_list.append(price)
                sell_list.append(np.nan)
                # set the flag to 1 to singal that the share was bought
                flag = 1

            elif ncf['Signal Line'][i] < ncf['MACD'][i] and flag == 1 and price > last_buy_price:
                buy_list.append(np.nan)
                sell_list.append(price)
                # Set the Flag to 0 to signal that the share was sold
                flag = 0
            else:
                buy_list.append(np.nan)
                sell_list.append(np.nan)
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

        # Update the new levels
        upper_lvl, lower_lvl = getlevels(price)

    return buy_list, sell_list


# Create buy and sell columns
buy, sell = strategy(df)
ncf['Buy_Signal_Price'] = buy
ncf['Sell_Signal_Price'] = sell
# Show data
# print(ncf)

# Plot the fibonacci levels along with the

new_df = ncf

plt.figure(figsize=(12.33, 4.5))
plt.plot(new_df.index, new_df['Close'], alpha=0.5)
plt.scatter(new_df.index, new_df['Buy_Signal_Price'],
            color='green', marker='^', alpha=1)
plt.scatter(new_df.index, new_df['Sell_Signal_Price'],
            color='red', marker='v', alpha=1)
plt.axhline(max_price, linestyle='--', alpha=0.5, color='red')
plt.axhline(first_level, linestyle='--', alpha=0.5, color='orange')
plt.axhline(second_level, linestyle='--', alpha=0.5, color='yellow')
plt.axhline(third_level, linestyle='--', alpha=0.5, color='green')
plt.axhline(fourth_level, linestyle='--', alpha=0.5, color='blue')
plt.axhline(min_price, linestyle='--', alpha=0.5, color='purple')
plt.ylabel('Clsoe Price in HKD')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.show()
#ncf.to_csv('09988.csv', index=False)
# print(new_core_five)
