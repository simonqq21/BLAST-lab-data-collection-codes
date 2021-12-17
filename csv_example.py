import pandas as pd

filename = "example.csv"
data1 = {'date': ["1/1/2022"], 'c1': ["data1"], 'c2': ["data2"]}
data2 = {'date': ["1/2/2022"], 'c1': ["data3"], 'c2': ["data4"]}

df1 = pd.DataFrame.from_dict(data1, orient='columns')
print(df1)
df2 = pd.DataFrame.from_dict(data2, orient='columns')
dfconcat = pd.concat([df1, df2])
print(df2)
print(dfconcat)
df1.to_csv('example.csv', mode='a', index=False, header=False)
df2.to_csv('example.csv', mode='a', index=False, header=False)
