# day23 > 2_군집_분석.py

import pandas as pd
import math
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

retail_df = pd.read_excel("Online_Retail.xlsx")
# print(retail_df.head())
"""
  InvoiceNo StockCode  ... CustomerID         Country
0    536365    85123A  ...    17850.0  United Kingdom
1    536365     71053  ...    17850.0  United Kingdom
2    536365    84406B  ...    17850.0  United Kingdom
3    536365    84029G  ...    17850.0  United Kingdom
4    536365    84029E  ...    17850.0  United Kingdom
"""

# print(retail_df.info())
"""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 541909 entries, 0 to 541908
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    541909 non-null  object        
 1   StockCode    541909 non-null  object        
 2   Description  540455 non-null  object        
 3   Quantity     541909 non-null  int64         
 4   InvoiceDate  541909 non-null  datetime64[ns]
 5   UnitPrice    541909 non-null  float64       
 6   CustomerID   406829 non-null  float64       
 7   Country      541909 non-null  object        
dtypes: datetime64[ns](1), float64(2), int64(1), object(4)
memory usage: 33.1+ MB
"""

retail_df = retail_df[retail_df["Quantity"]>0]
retail_df = retail_df[retail_df["UnitPrice"]>0]
retail_df = retail_df[retail_df["CustomerID"].notnull()]
retail_df["CustomerID"] = retail_df["CustomerID"].astype(int)

# print(retail_df.info())
"""
<class 'pandas.core.frame.DataFrame'>
Index: 397884 entries, 0 to 541908
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    397884 non-null  object        
 1   StockCode    397884 non-null  object        
 2   Description  397884 non-null  object        
 3   Quantity     397884 non-null  int64         
 4   InvoiceDate  397884 non-null  datetime64[ns]
 5   UnitPrice    397884 non-null  float64       
 6   CustomerID   397884 non-null  int64         
 7   Country      397884 non-null  object        
dtypes: datetime64[ns](1), float64(1), int64(2), object(4)
memory usage: 27.3+ MB
"""
# print(retail_df.isnull().sum())
"""
InvoiceNo      0
StockCode      0
Description    0
Quantity       0
InvoiceDate    0
UnitPrice      0
CustomerID     0
Country        0
dtype: int64
"""
# print(retail_df.shape)  # (397884, 8)

retail_df.drop_duplicates(inplace = True)
# print(retail_df.shape)  # (392692, 8)

new_ratail_df = pd.DataFrame([{"Product":len(retail_df["StockCode"].value_counts()),
               "Transaction" : len(retail_df["InvoiceNo"].value_counts()),
               "Customer" : len(retail_df["CustomerID"].value_counts())}],
             columns= ["Product", "Transaction", "Customer"], index = ["counts"])

# print(new_ratail_df)
"""
        Product  Transaction  Customer
counts     3665        18532      4338
"""

# print(retail_df["Country"].value_counts())
"""
Country
United Kingdom          349203
Germany                   9025
France                    8326
EIRE                      7226
Spain                     2479
Netherlands               2359
Belgium                   2031
Switzerland               1841
Portugal                  1453
Australia                 1181
Norway                    1071
Italy                      758
Channel Islands            747
Finland                    685
Cyprus                     603
Sweden                     450
Austria                    398
Denmark                    380
Poland                     330
Japan                      321
Israel                     245
Unspecified                241
Singapore                  222
Iceland                    182
USA                        179
Canada                     151
Greece                     145
Malta                      112
United Arab Emirates        68
European Community          60
RSA                         57
Lebanon                     45
Lithuania                   35
Brazil                      32
Czech Republic              25
Bahrain                     17
Saudi Arabia                 9
Name: count, dtype: int64
"""

retail_df["SaleAmount"] = retail_df["UnitPrice"] * retail_df["Quantity"]
# print(retail_df.head())
"""
  InvoiceNo StockCode  ...         Country  SaleAmount
0    536365    85123A  ...  United Kingdom       15.30
1    536365     71053  ...  United Kingdom       20.34
2    536365    84406B  ...  United Kingdom       22.00
3    536365    84029G  ...  United Kingdom       20.34
4    536365    84029E  ...  United Kingdom       20.34
"""

aggregations = {
    "InvoiceNo" : "count",
    "SaleAmount" : "sum",
    "InvoiceDate" : "max"
}

customer_df = retail_df.groupby("CustomerID").agg(aggregations)
customer_df = customer_df.reset_index()
# print(customer_df.head())
"""
   CustomerID  InvoiceNo  SaleAmount         InvoiceDate
0       12346          1    77183.60 2011-01-18 10:01:00
1       12347        182     4310.00 2011-12-07 15:52:00
2       12348         31     1797.24 2011-09-25 13:13:00
3       12349         73     1757.55 2011-11-21 09:51:00
4       12350         17      334.40 2011-02-02 16:01:00
"""

customer_df = customer_df.rename(columns = {"InvoiceNo" : "Freq", "InvoiceDate" : "ElapsedDays"})
# print(customer_df.head())
"""
   CustomerID  Freq  SaleAmount          ElapsedDays
0       12346     1    77183.60 2011-01-18 10:01:00
1       12347   182     4310.00 2011-12-07 15:52:00
2       12348    31     1797.24 2011-09-25 13:13:00
3       12349    73     1757.55 2011-11-21 09:51:00
4       12350    17      334.40 2011-02-02 16:01:00
"""

customer_df["ElapsedDays"] = datetime.datetime(2011,12,10) - customer_df["ElapsedDays"]
# print(customer_df.head())
"""
   CustomerID  Freq  SaleAmount        ElapsedDays
0       12346     1    77183.60 325 days 13:59:00
1       12347   182     4310.00   2 days 08:08:00
2       12348    31     1797.24  75 days 10:47:00
3       12349    73     1757.55  18 days 14:09:00
4       12350    17      334.40 310 days 07:59:00
"""

customer_df["ElapsedDays"] = customer_df["ElapsedDays"].apply(lambda x : x.days + 1)
# print(customer_df.head())
"""
   CustomerID  Freq  SaleAmount  ElapsedDays
0       12346     1    77183.60         326
1       12347   182     4310.00           3
2       12348    31     1797.24          76
3       12349    73     1757.55          19
4       12350    17      334.40         311
"""

fig, ax = plt.subplots()

ax.boxplot([customer_df["Freq"], customer_df["SaleAmount"], customer_df["ElapsedDays"]], sym="bo")
plt.xticks([1, 2, 3], ["Freq", "SaleAmount", "ElapsedDays"])
plt.show()

customer_df["Freq_log"] = np.log1p(customer_df["Freq"])
customer_df["SaleAmount_log"] = np.log1p(customer_df["SaleAmount"])
customer_df["ElapsedDays_log"] = np.log1p(customer_df["ElapsedDays"])
# print(customer_df.head())
"""
   CustomerID  Freq  SaleAmount  ...  Freq_log  SaleAmount_log  ElapsedDays_log
0       12346     1    77183.60  ...  0.693147       11.253955         5.789960
1       12347   182     4310.00  ...  5.209486        8.368925         1.386294
2       12348    31     1797.24  ...  3.465736        7.494564         4.343805
3       12349    73     1757.55  ...  4.304065        7.472245         2.995732
4       12350    17      334.40  ...  2.890372        5.815324         5.743003
"""

fig, ax = plt.subplots()

ax.boxplot([customer_df["Freq_log"], customer_df["SaleAmount_log"], customer_df["ElapsedDays_log"]], sym="bo")
plt.xticks([1, 2, 3], ["Freq_log", "SaleAmount_log", "ElapsedDays_log"])
plt.show()

X_features = customer_df[["Freq_log", "SaleAmount_log", "ElapsedDays_log"]].values
X_features_scaled = StandardScaler().fit_transform(X_features)

distortions = []

for i in range(1, 11):
    kmeans_i = KMeans(n_clusters=i, random_state=0)
    kmeans_i.fit(X_features_scaled)
    distortions.append(kmeans_i.inertia_)

plt.plot(range(1, 11), distortions, marker = "o")
plt.xlabel("Number of clusters")
plt.ylabel("Distortion")
plt.show()

kmeans = KMeans(n_clusters= 3, random_state=0)
Y_labels = kmeans.fit_predict(X_features_scaled)

customer_df["ClusterLabel"] = Y_labels
# print(customer_df.head())
"""
   CustomerID  Freq  SaleAmount  ...  SaleAmount_log  ElapsedDays_log  ClusterLabel
0       12346     1    77183.60  ...       11.253955         5.789960             2
1       12347   182     4310.00  ...        8.368925         1.386294             1
2       12348    31     1797.24  ...        7.494564         4.343805             2
3       12349    73     1757.55  ...        7.472245         2.995732             2
4       12350    17      334.40  ...        5.815324         5.743003             0

[5 rows x 8 columns]
"""