import pandas as pd

# data = {'col1': ['a0', 'b0', 'c0'],
#         'col2': ['a1', 'b1', 'c1']}
#
# df = pd.DataFrame(data)
# data2 = ['a2'] * df.shape[0]
# df['col3'] = data2
# print(df)

# data = {'role': [], 'datetime': [], 'sitename': [], 'hostname': [], 'lightintensity': []}
data = {'datetime': [], 'sitename': [], 'hostname': [], 'lightintensity': []}
df = pd.DataFrame.from_dict(data, orient='columns')
mode = 'w'
index=False
header=True
# df.to_csv('a.csv', mode=mode, index=index, header=header)
columns = pd.read_csv('a.csv').columns
newcolumns = df.columns
print(columns)
print(newcolumns)
diff = newcolumns.symmetric_difference(columns)
print(diff)

# for value in columns == df.columns.values:
#     if value == False:
#         print('error')
# print()
