"""Main module."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def set_style():
    sns.set()
    if 'ciyer' in mpl.style.available:
        plt.style.use(['seaborn-darkgrid', 'ciyer'])
    font = {'size': 20}
    mpl.rc('font', **font)
