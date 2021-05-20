import pandas as pd
import numpy as np
import scipy

import statsmodels.formula.api as smf

# %%
def read_df(path):
    df = pd.read_csv(path)
    df['TIME'] = pd.to_datetime(df['TIME'])
    return df


def df_to_ser(df, name):
    tdf = df[df['FREQUENCY'] == 'A'].set_index(["LOCATION", "TIME"])
    tdf = tdf.sort_index()
    ser = tdf['Value']
    ser.name = name
    return ser


def read_ser(path, name):
    df = read_df(path)
    return df_to_ser(df, name)


def ue_cpi_df(ue_ser, cpi_ser):
    m_df = pd.concat([ue_ser, cpi_ser], axis=1)
    diff_m_df = 100 * m_df.diff() / m_df.shift(1)
    diff_m_df.columns = [f"c_ue", "c_cpi"]
    m_df = m_df.join(diff_m_df).dropna()
    return m_df


# %%
ue_df = read_df("data/oecd/UE-2021.csv")
ue_df = ue_df[ue_df['SUBJECT'] == "TOT"]
ue_ser = df_to_ser(ue_df, "UE")
if len(ue_ser[ue_ser.index.duplicated()]):
    print("ue_ser contains duplicates")
    print(ue_ser[ue_ser.index.duplicated()])
ue_ser.head()


# %%
cpi_df = read_df("data/oecd/CPI-2021.csv")
cpi_df = cpi_df[cpi_df['SUBJECT'] == "TOT"]
cpi_df = cpi_df[cpi_df['MEASURE'] == "IDX2015"]
cpi_ser = df_to_ser(cpi_df, "CPI")
if len(cpi_ser[cpi_ser.index.duplicated()]):
    print("cpi_ser contains duplicates")
    print(cpi_ser[cpi_ser.index.duplicated()])
cpi_ser.head()

# %%
df = ue_cpi_df(ue_ser, cpi_ser)
# Only take from 1960 onwards
df = df.loc[(slice(None), slice("1960", "2021")), :]
df.head()


# %%
df.to_csv("data/phillips-ue-cpi.csv")

# %%
# Peak at the data if running interactively
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set()
# tdf = df.reset_index()
# tdf = tdf[tdf['TIME'] > "1999"]
# g = sns.FacetGrid(tdf, col='LOCATION', col_wrap=5)
# g.map(sns.scatterplot, "UE", "c_cpi")
