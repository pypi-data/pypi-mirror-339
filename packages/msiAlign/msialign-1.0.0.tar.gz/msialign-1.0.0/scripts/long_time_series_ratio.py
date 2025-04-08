import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import multiprocessing as mp
import re
from scripts.to1d import get_mz_int_depth, get_chunks, to_1d


def process_file(i):
    target_cmpds = {'levo': 185.0425, 'coronene': 300.09335,'C16': 279.22945, 'C18': 307.26075,
                    'C14': 251.19815, 'C12': 223.16685}
    sqlite_db_path = '/Users/weimin/Projects/projects/SBB14TC/metadata.db'
    how = "(data['int_levo'].sum()+ data['int_coronene'].sum()) / (data['int_levo'].sum() +data['int_C12'].sum()+ data['int_C14'].sum()+ data['int_C16'].sum() + data['int_C18'].sum() +data['int_coronene'].sum())"
    tol = 0.01
    min_snr = 1
    min_int = 10000
    min_n_samples = 10
    horizon_size = 400  # um
    horizon_size = horizon_size / 10000  # cm

    if 'PAH' in i:
        txts = os.listdir(f'/Users/weimin/Projects/projects/SBB14TC/PAH/msiAlign/{i}/export_da')
        txts = [txt for txt in txts if txt.endswith('.txt')]
        dfs = []
        for path in txts:
            df0 = get_mz_int_depth(
                os.path.join('/Users/weimin/Projects/projects/SBB14TC/PAH/msiAlign', i, 'export_da', path)
                , sqlite_db_path, target_cmpds, tol, min_snr, min_int, normalization=False)
            df0 = df0.replace(0, np.nan)
            df0 = df0.dropna()
            df0 = df0.sort_values(by='d')
            chunks = get_chunks(df0['d'], horizon_size, min_n_samples)
            depth_1d = to_1d(df0, chunks, "data['d'].mean()")
            mz_1d = to_1d(df0, chunks, how)
            horizon_count = [chunk[1] - chunk[0] for chunk in chunks]
            mz_1d = pd.DataFrame(mz_1d)
            df = pd.DataFrame({'d': depth_1d, 'horizon_count': horizon_count})
            df = pd.concat([df, mz_1d], axis=1)
            age_model = pd.read_csv(f'/Users/weimin/Projects/projects/SBB14TC/PAH/msiAlign/{i}/age.csv', index_col=0)
            age_model = age_model.reset_index()
            age_model.columns = ['year', 'index', 'd']
            age_model = age_model.astype(float)
            age_model = age_model.drop(columns='index')
            df['age'] = np.interp(df['d'], age_model['d'] / 10, age_model['year'])
            # df = df.dropna()
            df = df.sort_values(by='age')
            # give this a unique identifier
            df['R'] = path
            dfs.append(df)
        dfs = pd.concat(dfs)
        return dfs


if __name__ == "__main__":
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_file, os.listdir('/Users/weimin/Projects/projects/SBB14TC/PAH/msiAlign'))
    results = [result for result in results if result is not None]
    dfs = pd.concat(results)
    dfs = dfs.sort_values(by='age')
    # drop the columns where there are all nan
    dfs = dfs.dropna(axis=1, how='all')
    dfs = dfs.replace(0, np.nan)
    dfs = dfs.sort_values(by='age')

    cmpds = pd.read_csv('/Users/weimin/Projects/projects/SBB14TC/cmpds.csv')

    # fit a lowess model to the time series data
    from statsmodels.nonparametric.smoothers_lowess import lowess

    # fit a lowess model to the time series data
    import seaborn as sns

    Ti = pd.read_csv('/Users/weimin/Projects/projects/SBB14TC/XRF_Itrax/K.csv')

    fig, ax = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    x = dfs['age']
    y = dfs[0]
    z = lowess(y, x, frac=0.02)
    # plt.xlim(1500,1750)
    ax[0].plot(x, y)
    ax[0].plot(z[:, 0], z[:, 1])
    ax[0].set_ylabel('7-ring / 5-ring ratio')
    ax[1].plot(Ti['age'], Ti['Ti'])
    z2 = lowess(Ti['Ti'], Ti['age'], frac=0.02)
    ax[1].plot(z2[:, 0], z2[:, 1])

    ax[1].set_xlabel('Year')
    plt.tight_layout()
    plt.savefig('/Users/weimin/Desktop/7_5_ratio.png')
    plt.show()

    dfs['Ti'] = np.interp(dfs['age'], Ti['age'], Ti['Ti'])
    plt.plot(dfs['age'], dfs['Ti'])
    plt.xlabel('Ti')
    plt.ylabel('7-ring / 5-ring ratio')
    plt.tight_layout()
    plt.savefig('/Users/weimin/Desktop/Ti_7_5_ratio.png')
    plt.show()
