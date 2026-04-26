import pandas as pd
df = pd.read_csv('attacks.csv')
print(df["salida"].value_counts())