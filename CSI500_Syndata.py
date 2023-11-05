import pandas as pd
import yfinance as yf
import random

def generate_random_price(high, low):
    return random.uniform(low, high)

csi500_l1 = list(pd.read_csv("Yfinance_csi500_list.csv")['Code'])  #https://www.csindex.com.cn/#/indices/family/detail?indexCode=000905 composition with exchange code (SS/SZ) for yfinance
data_frames = []
csi500_l1.remove('601136.SS') # data unavailable

for stock in csi500_l1:
    data_frames.append(yf.download(stock, start="2022-04-01", end="2022-07-31"))

index_data = yf.download("ASHS", start="2022-04-08", end="2022-07-31",period='1d')

# transforming 1d ohlc to 30min close only data using randomness
transformed_df = []

for df in data_frames:
    transformed_data = []
    for index, row in df.iterrows():
        date = index
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        adj_close_price = row['Adj Close']

        # 6 random prices between high and low
        random_prices = [generate_random_price(high_price, low_price) for _ in range(6)]
        # allot values
        data = [
            {'Datetime': date.replace(hour=9, minute=30), 'Close': open_price},  # 1d open price
            {'Datetime': date.replace(hour=10), 'Close': random_prices[0]},
            {'Datetime': date.replace(hour=10, minute=30), 'Close': random_prices[1]},
            {'Datetime': date.replace(hour=11), 'Close': random_prices[2]},
            {'Datetime': date.replace(hour=13, minute=30), 'Close': random_prices[3]},
            {'Datetime': date.replace(hour=14),  'Close': random_prices[4]},
            {'Datetime': date.replace(hour=14, minute=30),  'Close': random_prices[5]},
            {'Datetime': date.replace(hour=14, minute=57), 'Close': close_price} # 1d close price
        ]

        transformed_data.extend(data)

    transformed_df.append(pd.DataFrame(transformed_data))


#combining them
final_df = pd.DataFrame()
final_df['Datetime'] = transformed_df[1]['Datetime']
for i in range(0,len(csi500_l1)):
    final_df[csi500_l1[i]] = transformed_df[i]['Close']

final_df.to_csv('CSI500_data.csv')
index_data.to_csv('CSI500_index.csv')