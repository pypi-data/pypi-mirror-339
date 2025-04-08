target_cmpds = {
    'GDGT_0': 1324.3046,
    'GDGT_5': 1314.2264
}
exported_txt_path = '/Users/weimin/Downloads/MV0811-14TC_5-10_Q1_1320_w40_75DR.d.d.txt'  # path to the exported txt file
sqlite_db_path = '/Users/weimin/Downloads/metadata.db'  # path to the sqlite database
how = "data['Int_GDGT_5'].sum() / (data['Int_GDGT_5'].sum() + data['Int_GDGT_0'].sum())"
tol = 0.01  # tolerance for the m/z value from the target m/z value
min_snr = 1  # minimum signal-to-noise ratio for the compound to be considered
min_int = 10000  # minimum intensity for the compound to be considered
min_n_samples = 10  # minimum number of samples in each horizon
