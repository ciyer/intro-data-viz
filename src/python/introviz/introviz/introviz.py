"""Main module."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def set_style():
    sns.set()
    if 'ciyer' in mpl.style.available:
        plt.style.use(['seaborn-darkgrid', 'ciyer'])
    else:
        plt.style.use(['seaborn-darkgrid'])
        p = sns.color_palette()
        sns.set_palette([p[0], p[3], p[8], p[2], p[7], p[4]])
    font = {'size': 20}
    mpl.rc('font', **font)
