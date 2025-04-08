import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import multiprocessing as mp
import re
from scripts.to1d import get_mz_int_depth, get_chunks, to_1d


def process_file(i):
    target_cmpds = {'levo':185.0421,'pyrene':265.2502}
    sqlite_db_path = '/Users/weimin/Projects/projects/SBB14TC/metadata.db'
    how = "data['int_levo'].sum() / (data['int_pyrene'].sum() + data['int_levo'].sum())"
    tol = 0.01
    min_snr = 1
    min_int = 10000
    min_n_samples = 10
    horizon_size = 200  # um
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
    x = dfs['age']
    y = dfs[0]
    z = lowess(y, x, frac=0.05)
    plt.plot(x, y, label='data')
    plt.plot(z[:, 0], z[:, 1], label='lowess')
    plt.legend()
    plt.show()