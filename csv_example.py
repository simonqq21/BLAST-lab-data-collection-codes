import pandas as pd

filename = "example.csv"
# data1 = {'date': ["1/1/2022"], 'c1': ["data1"], 'c2': ["data2"]}
data1 = {'date': [], 'c1': [], 'c2': []}
data2 = {'date': ["1/2/2022"], 'c1': ["data3"], 'c2': ["data4"]}

df1 = pd.DataFrame.from_dict(data1, orient='columns')
print(df1)
df2 = pd.DataFrame.from_dict(data2, orient='columns')
dfconcat = pd.concat([df1, df2])
dfconcat = pd.DataFrame(data1)
print(df2)
print(dfconcat)
# df1.to_csv('example.csv', mode='a', index=False, header=False)
# df2.to_csv('example.csv', mode='a', index=False, header=False)
dfconcat.to_csv('example.csv', mode='w', index=False)
df3 = pd.read_csv('example.csv')
print()
print(df3)
df3 = pd.concat([df3, df1, df2])
print(df3)
print(df3.columns)
data2 = [["12/2/2022", "data3", "data4"]]
print(df3.columns.values)
df4 = pd.DataFrame(data2, columns=df3.columns.values)
print(df4)
df3.to_csv('example.csv', mode='a', index=False, header=False)
