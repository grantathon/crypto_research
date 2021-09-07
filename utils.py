import pandas as pd

def format_cg_num_series(cg_series, fill_method=None):
    # Format data into a series
    s_dict = {}
    for r in cg_series:
        d = pd.to_datetime(r[0], unit='ms').date()
        v = float(r[1])

        # Ignore older, duplicate dates
        if(d not in s_dict.keys()):
            s_dict[d] = v
    s = pd.Series(s_dict, dtype='float64')

    # Fill in missing data
    if(fill_method is not None):
        if(fill_method == 'ffill'):
            d_range = pd.date_range(min(s.index), max(s.index))
            s = s.reindex(d_range, method='ffill')
        else:
            raise ValueError("Fill method isn't supported")

    return s
