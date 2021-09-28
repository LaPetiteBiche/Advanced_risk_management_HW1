import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('data/HFData_sample201801_v2.csv')

begin = 20180131
ap_int = 0
daily_ap = []
count = 0
date = ['20180102']

# Keep only Volume = 1 otherwise take eternity to compute -> Good enough estimation
df = df[df['VOLUME'] == 1]
# drop useless to gain on computation speed
df = df.drop("EXPIRATION",axis=1)
df = df.drop("year",axis=1)
df = df.drop("EXPIRY",axis=1)
df = df[df['date1']>=20180131]

for index, row in df.iterrows() :
    # Check same day
    if row['date1'] == begin :
        # 1 min after transaction
        time_1m = row[0]+60
        # Keep only 1 min recent
        df2 = df[df['DATETIME'] <= time_1m]
        # Select last transaction price in the 1 min
        price_1min = df2.iloc[-1, 4]
        # Compute return
        rit = abs((price_1min-row['PRICE'])/row['PRICE'])
        # Price
        price = row['PRICE']
        # Volume -> We only keep Volume = 1 for computation time
        volume = row['VOLUME']
        # Amihud price for each transaction
        ap_int += rit/(price*volume)
        count += 1

    # If new day
    elif row['date1'] != begin:
        # Save value in list and divide by total number
        daily_ap.append(ap_int / count)

        plt.plot(date, daily_ap, label="Daily Realized Spread")
        plt.show()
        plt.close()

        # Re initialize value
        ap_int = 0
        count = 0
        date.append(str(row['date1']))
        print(daily_ap)

        time_1m = row[0] + 60
        # Keep only 1 min recent
        df2 = df[df['DATETIME'] <= time_1m]
        # Select last transaction price in the 1 min
        price_1min = df2.iloc[-1, 4]
        # Compute return
        rit = abs((price_1min - row['PRICE']) / row['PRICE'])
        # Price
        price = row['PRICE']
        # Volume -> We only keep Volume = 1 for computation time
        volume = row['VOLUME']
        # Amihud price for each transaction
        ap_int += rit / (price * volume)
        count += 1

    # Adjust comparison for day
    begin = row['date1']
daily_ap.append(ap_int / count)

plt.plot(date, daily_ap, label="Daily Realized Spread")
plt.show()
plt.close()

# Re initialize value
ap_int = 0
count = 0
date.append(str(row['date1']))
print(daily_ap)