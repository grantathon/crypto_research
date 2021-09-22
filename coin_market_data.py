import json
import data

if __name__ == '__main__':
    # Load config file
    with open('configs/market_data_config.json') as f:
        config = json.load(f)

    # Prepare script parameters
    start_date = config['start_date']
    end_date = config['end_date']
    coin_cg_ids = config['coins']

    # Get data and save locally
    coin_data = data.coin_market_data(coin_cg_ids, start_date, end_date)
    coin_data.to_csv('output/coin_market_data.csv')
