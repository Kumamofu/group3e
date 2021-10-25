import pandas as pd

df_neko = pd.read_csv("output.csv")
# nekoze==1のFrameNoを抽出
rows = df_neko.loc[df_neko['nekoze'] == 1, 'FrameNo']
# print(rows)
