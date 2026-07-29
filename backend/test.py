import pandas as pd

df = pd.read_csv(
    "../dataset/EBM.csv",
    sep=";"
)

print(df.columns.tolist())
print(len(df))