import pandas as pd
import os
df = pd.read_csv("OldAccStatus.csv", index_col=0)

sample = len(df)

df = df[df['alive'] == True]

alive = len(df)

df = df[df['conections'].notna()]

has_cons = len(df)

no_cons = alive - has_cons

total = len(list(os.listdir(r"X:\Profiles")))

print(f"Sample size: {sample}, total: {total}")
print(f"Sample with cons: {has_cons}, total con estimation: {round(total*has_cons/sample)}")
print(f"Sample without cons: {no_cons}, total con-less estimation: {round(total*no_cons/sample)}")