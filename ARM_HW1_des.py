import pandas as pd
from matplotlib import pyplot as plt
# Import Data
df = pd.read_csv('data/HFData_sample201801_v2.csv')
print(df.head())

# Function for quoted bid-ask spread
def quoted_bid_ask(ask, bid):
    bid_ask = (ask-bid)/((ask+bid)/2)
    return bid_ask

# Function for midprice / mid quote
def midprice(ask, bid):
    bid_ask = (ask+bid)/2
    return bid_ask

# function realized spread
def effective_spread(price, mid, buy):
    if buy == 1:
        rs = 2 * (price - mid)
    else:
        rs = 2 * (mid - price)
    return abs(rs)

begin = 20180102
rs_int = 0
daily_rs = []
count = 0
date = ['20180102']
# Keep only Volume = 1 otherwise take eternity to compute -> Good enough estimation
df = df[df['VOLUME'] == 1]
# drop useless to gain on computation speed
df = df.drop("EXPIRATION",axis=1)
df = df.drop("year",axis=1)
df = df.drop("VOLUME",axis=1)
df = df.drop("EXPIRY",axis=1)

# Daily realized spread
for index, row in df.iterrows() :
    # Check same day and only market order
    if row['date1'] == begin and row['MARKET_ORDER'] == 'Y':
        # Search for next sale/buy
        df2 = df[df['DATETIME'] >= row[0]]
        if row['BUY'] == 1 :
            df2 = df2[df2['BUY'] == 0]
            next = df2.iloc[0,4]
        if row['BUY'] == 0 :
            df2 = df2[df2['BUY'] == 1]
            next = df2.iloc[0,4]

        # Price
        price = row['PRICE']
        # Effective spread for transaction
        rs_int += effective_spread(price, next, row['BUY'])
        count += 1

    # If new day
    elif row['date1'] != begin :
        # Save value in list and divide by total number
        daily_rs.append(rs_int/count)

        plt.plot(date, daily_rs, label="Daily Realized Spread")
        plt.show()
        plt.close()

        # Re initialize value
        rs_int = 0
        count = 0
        date.append(str(row['date1']))
        print(daily_rs)
        if row[-1] == 'Y':
            df2 = df[df['DATETIME'] >= row[0]]
            if row['BUY'] == 1:
                df2 = df2[df2['BUY'] == 0]
                next = df2.iloc[0, 4]
            if row['BUY'] == 0:
                df2 = df2[df2['BUY'] == 1]
                next = df2.iloc[0, 4]
            # Price
            price = row['PRICE']
            # Effective spread for transaction
            rs_int += effective_spread(price, next, row['BUY'])
            count += 1

    # Adjust comparison for day
    begin = row['date1']