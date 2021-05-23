import pandas as pd
import numpy as np
import scipy


df_2000_2020 = pd.read_csv("data/mortality-fr/morts_2020-05-18.csv")
df_2000_2020 = df_2000_2020.set_index('mois_jour')

df_2019_2021_cuml = pd.read_csv("data/mortality-fr/2021-05-21_deces_quotidiens_departement_csv.txt", sep=";")
df_2019_2021_cuml = df_2019_2021_cuml[df_2019_2021_cuml['Zone'] == 'France']


# Just keep the columns we need
df_2019_2021_cuml = df_2019_2021_cuml[['Date_evenement', 'Total_deces_2019', 'Total_deces_2020', 'Total_deces_2021']]


# Extract the day/month
date_names = df_2019_2021_cuml['Date_evenement'].str.split('-')
df_2019_2021_cuml['day'] = date_names.apply(lambda x: x[0])
df_2019_2021_cuml['monthname'] = date_names.apply(lambda x: x[1])

monthname_map = {n:(i+1) for i, n in enumerate(df_2019_2021_cuml['monthname'].unique())}
df_2019_2021_cuml['month'] = df_2019_2021_cuml['monthname'].apply(lambda x: monthname_map[x])
df_2019_2021_cuml['mois_jour'] = df_2019_2021_cuml.apply(lambda row: f"{row['month']:02}/{row['day']}", axis=1)
df_2019_2021_cuml = df_2019_2021_cuml[['mois_jour', 'Total_deces_2019', 'Total_deces_2020', 'Total_deces_2021']]


# Conver the cumulative counts to quotidian
df_2019_2021 = df_2019_2021_cuml.set_index('mois_jour').diff()
df_2019_2021.iloc[0] = df_2019_2021_cuml.iloc[0][1:]
df_2019_2021.columns = ["2019", "2020", "2021"]

# The two series are close where they overlap, but not exactly equal. Use the Insee data where there is overlap
df = df_2000_2020.drop(["2019", "2020"], axis=1)
df = df.join(df_2019_2021)
df.to_csv("data/aux/mortality-fr.csv")
