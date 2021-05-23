import datetime

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.formula.api as smf
import statsmodels.api as sm

lowess = sm.nonparametric.lowess


def read_data(path="data/phillips-ue-cpi.csv"):
    df = pd.read_csv(path)
    df['TIME'] = pd.to_datetime(df['TIME'])
    df = df.set_index(['LOCATION', "TIME"])
    return df


def arrows(ax, df, x_col, y_col, color):
    for i in range(0, len(df.index) - 1):
        idx = df.index[i]
        idx_p1 = df.index[i+1]
        ax.annotate('',
                    xytext=(df.loc[idx, x_col], df.loc[idx, y_col]),
                    textcoords='data',
                    xy=(df.loc[idx_p1, x_col], df.loc[idx_p1, y_col]),
                    xycoords='data',
                    arrowprops=dict(arrowstyle="-|>", facecolor=color, alpha=0.5,
                        edgecolor=color),
                    color=color,
                    size=15)


def annotate_year(ax, year, df, x_col, y_col):
    y = str(year)
    try:
        ax.annotate(y, (df.loc[y, x_col], df.loc[y, y_col]))
    except:
        pass


def annotate_years(ax, df, xcol, ycol):
    start_year = df.index[0].year
    end_year = df.index[-1].year
    years_to_label = set([start_year, end_year])
    bp_year = start_year + 5 - (start_year % 5)
    for y in range(bp_year, 2021, 5):
        years_to_label.add(y)

    for y in years_to_label:
        annotate_year(ax, y, df, xcol, ycol)


def ols(df, x_col, y_col):
    lm = smf.ols(formula=f"{y_col} ~ {x_col}", data=df).fit()
    return lm


def regression(ax, df, x_col, y_col, color, label="regression", text_offset=(0,0)):
    lm = ols(df, x_col, y_col)
    pred_range = (df[x_col].min(), df[x_col].max())
    preds_input = pd.DataFrame({x_col: pred_range})
    predictions = lm.predict(preds_input)
    ax.plot(pred_range, predictions, color=color, alpha=0.7, lw=3.0, label=label)
    ax.text(pred_range[1]+text_offset[0], predictions[1]+text_offset[1], "$r^2={:.2f}$".format(lm.rsquared))


def yeqx(ax, tdf, xcol, ycol, color, lims, label="y = x"):
    l = np.linspace(lims[0], lims[1])
    ax.plot(l, l, color=color, alpha=0.4, lw=3.0, label=label)



def cite_source(ax, source):
    ax.annotate(f"Source: {source}", (1, 0), (-2, -30), fontsize=10,
                xycoords='axes fraction', textcoords='offset points', va='bottom', ha='right')



def ue_cpi_reg_df(m_df, col):
    regs = []
    for lctn in m_df.index.levels[0]:
        try:
            tdf = m_df.loc[lctn, :]
            lm = ols(tdf, col, 'c_cpi')
            regs.append({"LOCATION": lctn, "r2": lm.rsquared, "slope": lm.params.loc[col]})
        except KeyError as e:
            pass


    reg_df = pd.DataFrame(regs).set_index("LOCATION")
    reg_df = reg_df.sort_values("r2", ascending=False)
    reg_df["r2cat"] = pd.qcut(reg_df['r2'], 4, False)
    return reg_df



def xy_plot(ax, df, loc, xcol="UE", ycol="c_cpi", s_color=None, r_color=None, l_color=None, a_color=None, text_offset=(0, 0)):
    palette = sns.color_palette()
    s_color = palette[1] if not s_color else s_color
    r_color = palette[0] if not r_color else r_color
    l_color = palette[4] if not l_color else l_color
    a_color = palette[4] if not a_color else a_color
    tdf = df.loc[loc, :]
    ax.plot(tdf[xcol], tdf[ycol], alpha=0.5, color=l_color)
    arrows(ax, tdf, xcol, ycol, a_color)
    ax.scatter(tdf[xcol], tdf[ycol], alpha=0.6, s=80, color=s_color, label=loc)
    annotate_years(ax, tdf, xcol, ycol)
    regression(ax, tdf, xcol, ycol, r_color, loc, text_offset=text_offset)


def r2_df(df, x_col="UE", y_col="c_cpi"):
    r2s = []
    for loc, loc_df in df.groupby(level="LOCATION"):
        lm = ols(loc_df, x_col, y_col)
        r2s.append({"LOCATION": loc, "R2": lm.rsquared})
    return pd.DataFrame(r2s)


def facet_xy_plot_label(df, ue_cpi_r2_df, loc):
    tdf = df.loc[loc, :].reset_index()
    dr = tdf['TIME'].agg([np.min, np.max]).dt.year
    r2 = ue_cpi_r2_df[ue_cpi_r2_df['LOCATION'] == loc]['R2'].iloc[0]
    # title = f"{loc} | {dr['amin']} – {dr['amax']}\n$r^2 = {r2:.2f}$"
    title = f"{loc} | {dr['amin']} – {dr['amax']}"
    return title


def facet_xy_plot(xcol, ycol, color, **kwargs):
    data = kwargs['data'].set_index('TIME')
    loc = data.iloc[0]['LOCATION']
    ax = plt.gca()
    palette = sns.color_palette()
    s_color=palette[1]
    r_color=palette[0]
    l_color=palette[4]
    ax.plot(data[xcol], data[ycol], alpha=0.5, color=l_color)
    ax.scatter(data[xcol], data[ycol], alpha=0.6, s=80, color=s_color, label=loc)
    regression(ax, data, xcol, ycol, r_color, data.index, text_offset=(0, 0))
