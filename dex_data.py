import json
import data

if __name__ == '__main__':
    # Load config file
    with open('configs/dex_data_config.json') as f:
        config = json.load(f)

    # Prepare script parameters
    start_date = config['start_date']
    end_date = config['end_date']
    dex_cg_ids = [k for k in config['dex'].keys()]
    dex_coin_cg_ids = list(set([v['coin_id'] for v in config['dex'].values() if v['coin_id'] != '']))

    # Get data and save locally
    dex_data = data.dex_trading_volume(dex_cg_ids, start_date, end_date)
    dex_data.to_csv('output/dex_trading_volume.csv')
    coin_data = data.coin_market_data(dex_coin_cg_ids, start_date, end_date)
    coin_data.to_csv('output/dex_coin_market_data.csv')
