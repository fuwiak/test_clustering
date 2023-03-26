import pandas as pd


df = pd.read_excel('/Users/user/PycharmProjects/clustering_simple_analysis/data/Online Retail.xlsx')
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

now = pd.Timestamp('now')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Recency'] = (now - df['InvoiceDate']).dt.days


rfm = df.groupby('CustomerID').agg({'InvoiceDate': lambda x: (now - x.min()).days,
                                        'InvoiceNo': lambda x: len(x),
                                        'TotalSum': lambda x: x.sum()})

rfm.columns = ['Recency', 'Frequency', 'Monetary']
rfm['Recency'] = rfm['Recency'].astype(int)
rfm['Frequency'] = rfm['Frequency'].astype(int)
rfm['Monetary'] = rfm['Monetary'].astype(int)

# rfm['RecencyScore'] =pd.qcut(rfm['Recency'], q=10, labels=range(5, 0, -1), duplicates='drop')

num_labels = 5
rfm['RecencyScore'] = pd.qcut(rfm['Recency'], q=num_labels, labels=range(num_labels, 0, -1), duplicates='drop')
rfm['FrequencyScore'] = pd.qcut(rfm['Frequency'], q=num_labels, labels=range(1, num_labels + 1), duplicates='drop')
rfm['MonetaryScore'] = pd.qcut(rfm['Monetary'], q=num_labels, labels=range(1, num_labels + 1), duplicates='drop')


