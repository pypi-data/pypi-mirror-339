#! /usr/bin/env python
import sys
import os
import pandas as pd
from upsetplot import UpSet, from_indicators
import itertools
from scipy.stats import hypergeom
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

def upset_enrich(dat, 
    n_items, 
    plot_out="upset.pdf",
    p_thresh=0.01,
    max_subset=20,
    shading_color='#E8EDDF',
    bg_color='#000000',
    enrich_color='#F5CB5C'):
    """
    Read data, perform enrichment testing, and generate UpSet plot.
    
    data (first argument) should be a dict, with keys being names of sets
        and values being lists/sets of members.
    """

    # Read all as Pandas DataFrames
    dfs = []
    dfcount_1way = {'name': [], 'count': []}
    for name in dat.keys():
        datconv = []
        for i, elt in enumerate(dat[name]):
            datconv.append(str(elt))
        dfs.append(pd.DataFrame({'member': datconv, 'name': name, 'val': 1}))
        dfcount_1way['name'].append(name)
        dfcount_1way['count'].append(len(dat[name]))
    df = pd.concat(dfs, axis=0)
    df['val'] = df['val'].astype(int)
    
    #counts_1way = df.loc[df['val'] == 1,:]['name'].value_counts()\
    #    .reset_index(drop=False).rename({"index": "name"}, axis=1)
    counts_1way = pd.DataFrame(dfcount_1way)

    # Now need to cast
    df = pd.pivot(df, index='member', columns=['name'], values=['val']).fillna(0)
    df.index.name = None
    df.columns.name = None
    
    # Now need to find significant intersections
    thresh = p_thresh

    names1 = []
    names2 = []
    counts = []
    for col1, col2 in itertools.combinations(range(0, df.shape[1]), 2):
        name1 = df.columns[col1]
        name2 = df.columns[col2]
        names1.append(name1[1])
        names2.append(name2[1])
        counts.append(df.loc[(df[name1] == 1) & (df[name2] == 1),:].shape[0])
    
    counts_2way = pd.DataFrame({'name1': names1, 'name2': names2, 'overlap': counts})
    counts_2way = counts_2way.merge(counts_1way, left_on='name1', right_on='name')
    counts_2way = counts_2way.merge(counts_1way, left_on='name2', right_on='name').\
        drop(['name_x', 'name_y'], axis=1)
    hyper_vec = np.vectorize(hypergeom.cdf)
    counts_2way['p'] = 1-hyper_vec(counts_2way['overlap'], 
            [n_items] * counts_2way.shape[0],
            counts_2way['count_x'],
            counts_2way['count_y'])
    
    counts_2way = counts_2way.loc[counts_2way['p'] < thresh,:]

    name_all = set([])
    for name in counts_1way['name']:
        name_all.add(name)

    signifs = []
    signifs_not = []
    for _, row in counts_2way.iterrows():
        signifs.append([row['name1'], row['name2']])
        row_pos = set([row['name1'], row['name2']])
        row_neg = list(name_all.difference(row_pos))
        signifs_not.append(row_neg)

    n_names = df.shape[1]
    for n_comb in range(3, n_names+1):
        # Get all combinations with this many members
        combs = itertools.combinations(range(0, n_names), n_comb)
        n_pass = 0
        for comb in combs:
            tot = 0
            signif = 0
            for comb2 in itertools.combinations(comb, 2):
                n1 = df.columns[comb2[0]]
                n2 = df.columns[comb2[1]]
                if counts_2way.loc[(counts_2way['name1'] == n1[1]) & \
                    (counts_2way['name2'] == n2[1]),:].shape[0] > 0:
                    signif += 1
                tot += 1

            if tot == signif:
                # Accept this combination
                n_pass += 1
                grp = []
                for idx in comb:
                    grp.append(df.columns[idx][1])
                signifs.append(grp)
                grpset = set(grp)
                grp_not = list(name_all.difference(grpset))
                signifs_not.append(grp_not)
            else:
                grp = []
                for idx in comb:
                    grp.append(df.columns[idx][1])

        if n_pass == 0:
            # Won't see any next round either
            break

    # Now build the plot.
    df2 = {}
    for coln in df.columns:
        df2[coln[1]] = df[coln].astype('bool')
    df2 = pd.DataFrame(df2)

    matplotlib.rcParams['font.size'] = 9
    upset = UpSet(from_indicators(df2), subset_size='sum', 
            sort_by='cardinality', show_counts="{:.0f}",
            shading_color=shading_color,
            facecolor=bg_color,
            max_subset_rank=max_subset)
    for i in range(0, len(signifs)):
        upset.style_subsets(present=signifs[i], absent=signifs_not[i], 
            facecolor=enrich_color, label='all pairwise p < {}'.format(thresh))

    upset.plot()
    plt.savefig(plot_out, dpi=300)

