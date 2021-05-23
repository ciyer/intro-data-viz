import datetime

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


palette = sns.color_palette()

# %%
def read_data(path="data/mortality-covid-fr.csv"):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


def read_demo_data(path="data/demographics/france_demographics.csv"):
    demo_df = pd.read_csv(path)
    demo_df['population'] = pd.to_numeric(demo_df['Population'].str.replace(",", ""))
    demo_df = demo_df.drop('Population', axis=1)
    return demo_df.set_index('year')


def cite_source(ax, source="Baptiste Coulmont / Insee"):
    ax.annotate(f"Source: {source}", (1, 0), (-2, -30), fontsize=10,
                xycoords='axes fraction', textcoords='offset points', va='bottom', ha='right')


def plot_prepandemic_all_cause_mortality(ax, covid_df, pandemic_start, alpha=0.3, color=None, label="pre-pandemic"):
    palette = sns.color_palette()
    color = palette[4] if not color else color
    pre_pandemic_df = covid_df.loc["2000":pandemic_start, :].set_index(['mois_jour', 'year'])
    pre_pandemic_df = pre_pandemic_df['allcause_per100k'].unstack()
    for i, c in enumerate(pre_pandemic_df.columns):
        tser = pre_pandemic_df[c].reset_index(drop=True)
        lbl = label if i == 0 else None
        ax.plot(tser.index, tser, alpha=0.3, color=color, label=lbl)
    # Make 2003 a little more visible
    try:
        tser = pre_pandemic_df[2003].reset_index(drop=True)
        ax.plot(tser.index, tser, alpha=0.3, color=color)
        ax.annotate("2003 heatwave", (pd.to_datetime("2003-08-15").day_of_year, 5.8))
    except Exception as e:
        pass
    month_offset = [("jan", 0), ("feb", 31), ("mar", 28), ("apr", 31), ("may", 30),
        ("jun", 31), ("jul", 30), ("aug", 31), ("sep", 31), ("oct", 30), ("nov", 31), ("dec", 30)]
    tick_pos = np.array([o[1] for o in month_offset]).cumsum()
    tick_label = np.array([o[0] for o in month_offset])
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(tick_label)


def plot_pandemic_all_cause_mortality(ax, covid_df, pandemic_start, years=[2020, 2021], alpha=0.3, lw=3, color=None, label="pandemic"):
    palette = sns.color_palette()
    color = palette[1] if not color else color    
    pandemic_df = covid_df.loc[pandemic_start:, :].set_index(['mois_jour', 'year'])
    pandemic_df = pandemic_df['allcause_per100k'].unstack()
    for i, c in enumerate(years):
        tser = pandemic_df[c].reset_index(drop=True)
        lbl = label if i == 0 else None
        ax.plot(tser.index, tser, alpha=0.7, label=lbl, lw=3, color=color)


def plot_yearly_all_cause_mortality(ax, covid_df, pandemic_start, source="Baptiste Coulmont / Insee"):
    plot_prepandemic_all_cause_mortality(ax, covid_df, pandemic_start)
    plot_pandemic_all_cause_mortality(ax, covid_df, pandemic_start)
    cite_source(ax, source)
    ax.set_title("All-cause Daily Mortality per 100k, France Jan 2000 — May 2021")
    
    
def median_mortality_ser(covid_df):
    return covid_df.groupby('mois_jour').median()['allcause_per100k'].reset_index(drop=True)


def plot_median_mortality(ax, covid_df, alpha=0.6, lw=3, color='k', label="median"):
    all_cause_median_ser = median_mortality_ser(covid_df)
    ax.plot(all_cause_median_ser.index, all_cause_median_ser, alpha=alpha, label=label, lw=lw, color=color)


def plot_covid_mortality(ax, covid_df, pandemic_start, years=[2020, 2021], alpha=0.9, lw=3, color=None, label="median + covid"):
    palette = sns.color_palette()
    color = palette[3] if not color else color
    all_cause_median_ser = median_mortality_ser(covid_df)
    covid_per100k_df = covid_df.set_index(['mois_jour', 'year'], append=True)['covid_per100k']
    covid_per100k_df = covid_per100k_df.rolling(7).median().loc[pandemic_start:, :].shift(-7)
    covid_per100k_df = covid_per100k_df.reset_index(0, drop=True).unstack()
    for i, c in enumerate(years):
        tser = covid_per100k_df[c].reset_index(drop=True)
        lbl = label if i == 0 else None
        ax.plot(tser.index, all_cause_median_ser + tser, alpha=alpha, label=lbl, lw=lw, color=color)
        

def excess_mortality(covid_df, demo_df, start, end):
    """Return excess mortality to the nearest 1000 below"""
    mm_ser = median_mortality_ser(covid_df)
    mortality = covid_df.loc[start:end, 'allcause_per100k'].sum()
    expected_mortality = mm_ser.loc[start.day_of_year:end.day_of_year].sum()
    mortality_diff = mortality - expected_mortality
    year_pop = demo_df.loc[end.year, 'population']
    num_diff = mortality_diff * year_pop / 100000
    return np.floor(num_diff/1000.0) * 1000
