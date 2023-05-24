import pandas as pd

# initializing list
test_list = [(12, 'A', 'Gfg'), (23, 'H', 'Gfg'),
             (13, 'A', 'Best'), (18, 'A', 'Gfg'),
             (2, 'H', 'Gfg'), (23, 'A', 'Best')]

# creating a pandas DataFrame from the list
df = pd.DataFrame(test_list, columns=['value', 'key1', 'key2'])
print (df)
# grouping by key1 and key2 and summing the values
grouped = df.groupby(['key1', 'key2'])['value'].sum()

# converting the result back to a list of tuples
res = [(key[0], key[1], value) for key, value in grouped.items()]

# printing result
print("The grouped summation : " + str(res))
