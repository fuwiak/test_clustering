import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def create_rfm_dataset(df):
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]

    index = df['StockCode'].str.contains('C', na=False)
    df = df[~index]
    df = df.drop_duplicates()
    df = df.dropna()
    df = df.reset_index(drop=True)
    df['TotalSum'] = df['Quantity'] * df['UnitPrice']

    df['CustomerID'] = df['CustomerID'].astype(int)
    df['Quantity'] = df['Quantity'].astype(int)

    df = df.reset_index(drop=True)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])



    rfm = df.groupby('CustomerID').agg({'InvoiceDate': lambda x: (x.max() - x.min()).days,
                                        'InvoiceNo': lambda x: len(x),
                                        'TotalSum': lambda x: x.sum()})
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    rfm['Recency'] = rfm['Recency'].astype(int)
    rfm['Frequency'] = rfm['Frequency'].astype(int)
    rfm['Monetary'] = rfm['Monetary'].astype(int)
    return rfm

# df = pd.read_excel('/Users/user/PycharmProjects/clustering_simple_analysis/data/Online Retail.xlsx')
# rfm = create_rfm_dataset(df)
# print(rfm)


def rfm_segmentation(rfm):
    rfm['RecencyScore'] = pd.qcut(rfm['Recency'], 7, labels=[5, 4, 3, 2, 1],
                                  duplicates='drop')
    rfm['FrequencyScore'] = pd.qcut(rfm['Frequency'], 5)
    rfm['MonetaryScore'] = pd.qcut(rfm['Monetary'], 5)

    rfm['FrequencyScore'] = rfm['FrequencyScore'].cat.codes
    rfm['FrequencyScore'] = rfm['FrequencyScore'] + 1
    rfm['FrequencyScore'] = rfm['FrequencyScore'].astype(str)

    rfm['MonetaryScore'] = rfm['MonetaryScore'].cat.codes
    rfm['MonetaryScore'] = rfm['MonetaryScore'] + 1
    rfm['MonetaryScore'] = rfm['MonetaryScore'].astype(str)

    rfm['RFMScore'] = rfm['RecencyScore'].astype(str) + rfm[
        'FrequencyScore'].astype(str) + rfm['MonetaryScore'].astype(str)
    return rfm

# rfm = rfm_segmentation(rfm)
# Customer Segmentation by Recency and Frequency

def segmentation_map(rfm):
    seg_map = {
        r'[1-2][1-2]': 'Best Customers',
        r'[1-2][3-4]': 'Loyal Customers',
        r'[1-2]5': 'Big Spenders',
        r'3[1-2]': 'Almost Lost',
        r'33': 'Lost Customers',
        r'[3-4][4-5]': 'Lost Cheap Customers',
        r'41': 'Lost Cheap Customers',
        r'[4-5][2-3]': 'Lost Cheap Customers',
        r'51': 'Lost Cheap Customers',
        r'[4-5][4-5]': 'Lost Cheap Customers'
    }

    rfm['Segment'] = rfm['RecencyScore'].astype(str) + rfm[
        'FrequencyScore'].astype(str)
    rfm['Segment'] = rfm['Segment'].replace(seg_map, regex=True)

    return rfm

# rfm = segmentation_map(rfm)


