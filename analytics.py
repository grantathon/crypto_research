import pandas as pd
from pprint import pprint

def nvf(market_caps, trading_volumes, trade_fee, avg_window, ann_factor):
    # Calculate average annualized trading fees
    avg_trading_volumes = trading_volumes[trading_volumes > 0].rolling(window=avg_window).mean().dropna()
    annual_trading_fees = avg_trading_volumes * trade_fee * ann_factor

    # Calculate NVF
    return (market_caps / annual_trading_fees).dropna()
