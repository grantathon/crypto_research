import pandas as pd
import requests
import json
import time
from pprint import pprint

CG_API_URL = "https://api.coingecko.com/api/v3/"

def dex_trading_volume(cg_ids, start_date, end_date):
    df_dict = {}

    # Number of days we need for data call
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    today = pd.to_datetime('today')
    days = (today - start_date).days + 1

    # Get trading volume data per DEX
    for id in cg_ids:
        # Get raw data from API
        req_url = CG_API_URL + 'exchanges/' + id + '/volume_chart'
        res = requests.get(req_url, params={'days': days})
        res_json = res.json()

        # Format data into a series
        s_dict = {}
        for r in res_json:
            d = pd.to_datetime(r[0], unit='ms').date()
            v = float(r[1])

            # Ignore older, duplicate dates
            if(d not in s_dict.keys()):
                s_dict[d] = v

        # Create series and forward fill missing data (or set to zero?)
        s = pd.Series(s_dict, dtype='float64')
        d_range = pd.date_range(min(s.index), max(s.index))
        s = s.reindex(d_range, method='ffill')

        df_dict[id] = s
        time.sleep(3)  # CG API has call limits

    # Combine, trime, and export data
    df = pd.DataFrame(df_dict)
    df = df.loc[start_date:end_date]
    pprint(df)
    df.to_csv('dex_trading_volume.csv')

def dex_coin_market_data(cg_ids, start_date, end_date):
    pass

if __name__ == '__main__':
    # Load config file
    with open('configs/dex_data_config.json') as f:
        config = json.load(f)

    # Prepare script parameters
    start_date = config['start_date']
    end_date = config['end_date']
    dex_cg_ids = [k for k in config['dex'].keys()]
    dex_coin_cg_ids = list(set([v['coin_id'] for v in config['dex'].values() if v['coin_id'] != '']))

    dex_trading_volume(dex_cg_ids, start_date, end_date)
