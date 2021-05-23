import numpy as np
import pandas as pd


# %%
demo_df = pd.read_csv("data/demographics/france_demographics.csv")
demo_df['population'] = pd.to_numeric(demo_df['Population'].str.replace(",", ""))
demo_df = demo_df.drop('Population', axis=1)
demo_df.head()


# %%
pop100k_map = {str(row['year']): (row['population'] / 100000) for i, row in demo_df.iterrows()} 


# %%
fr_df = pd.read_csv("data/aux/mortality-fr.csv")

# drop Feb 29 -- it is not important and makes things messy
fr_df = fr_df.drop(59).reset_index(drop=True)
fr_df = fr_df.set_index('mois_jour').stack().reset_index()
fr_df.columns = ['mois_jour', 'year', 'allcause']
fr_df['date'] = pd.to_datetime(fr_df.apply(lambda x: f"{x['mois_jour']}/{x['year']}", axis=1))
fr_df['allcause_per100k'] = fr_df.apply(lambda x: x['allcause'] / pop100k_map[x['year']], axis=1)
fr_df.head()


# %%
covid_df = pd.read_csv("data/covid-19_jhu-csse/time_series_covid19_deaths_global.csv")
covid_df = covid_df[covid_df['Country/Region'] == 'France']
covid_df = covid_df[covid_df['Province/State'].isna()]

covid_df = covid_df.drop(['Country/Region', 'Province/State', 'Lat', 'Long'], axis=1)
covid_df = covid_df.unstack().reset_index(0)
covid_df.columns = ['date', 'covid']
covid_df['date'] = pd.to_datetime(covid_df['date'])
covid_df['covid_per100k'] = covid_df.apply(lambda x: x['covid'] / pop100k_map[str(x['date'].year)], axis=1)
covid_df = covid_df.set_index('date')
covid_df = covid_df.diff()


# %%
df = fr_df.set_index('date').join(covid_df).sort_index()


# %%
df.to_csv("data/mortality-covid-fr.csv")



