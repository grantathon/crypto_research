import pandas as pd
import utils
import time
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
API_SLEEP_TIME = 5

def dex_trading_volume(cg_ids, start_date, end_date):
    print('Getting DEX trading volume...')
    df_dict = {}

    # Number of days we need for data call
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    today = pd.to_datetime('today')
    days = (today - start_date).days + 1

    # Get trading volume data per DEX
    for id in cg_ids:
        res = cg.get_exchanges_volume_chart_by_id(id, days)

        # Format data
        s = utils.format_cg_num_series(res, fill_method='ffill')
        df_dict[id] = s

        print('- ' + id)
        time.sleep(API_SLEEP_TIME)  # CG API has call limits

    # Combine, trim, and export data
    df = pd.DataFrame(df_dict)
    df = df.loc[start_date:end_date]
    print('Got DEX trading volume')
    return df

def coin_market_data(cg_ids, start_date, end_date):
    print('Getting coin market data...')
    df_dict = {}

    # Number of days we need for data call
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    today = pd.to_datetime('today')
    days = (today - start_date).days + 1

    # TODO: Test this for shorter data requests
    if(days <= 91):
        days = 91

    # Get market data per DEX coin
    for id in cg_ids:
        res = cg.get_coin_market_chart_by_id(id=id, vs_currency='USD', days=days)

        # Format data
        s = utils.format_cg_num_series(res['prices'], fill_method='ffill')
        df_dict[id + ' price'] = s
        s = utils.format_cg_num_series(res['market_caps'], fill_method='ffill')
        df_dict[id + ' market caps'] = s

        print('- ' + id)
        time.sleep(API_SLEEP_TIME)  # CG API has call limits

    # Combine, trim, and export data
    df = pd.DataFrame(df_dict)
    df = df.loc[start_date:end_date]
    print('Got coin market data')
    return df
