import numpy as np
import pandas as pd
# from pprint import pprint

def nvf(market_caps, trading_volumes, trade_fee, avg_window, ann_factor):
    avg_trading_volumes = trading_volumes[trading_volumes > 0].rolling(window=avg_window).mean().dropna()
    annual_trading_fees = avg_trading_volumes * trade_fee * ann_factor
    return (market_caps / annual_trading_fees).dropna()

def total_return(prices):
    return (prices[-1] / prices[0]) - 1

def returns(prices, type='arith'):
    if(type == 'arith'):
        return prices.pct_change()[1:]
    elif(type == 'log'):
        return np.log(prices / prices.shift(1))[1:]
    else:
        raise ValueError("Return type %s is not supported." % (type))

def volatility(returns):
    return np.std(returns)

def pnl_performance(pnl, start_val):
    return pnl.cumsum() + start_val

def performance(returns):
    return (1 + returns).cumprod() - 1

def sharpe_ratio(returns, risk_free_rate, ann_factor):
    ann_ret = ann_factor * np.mean(returns)
    ann_vol = np.sqrt(ann_factor) * volatility(returns)
    return (ann_ret - risk_free_rate) / ann_vol

def information_ratio(portfolio_returns, benchmark_returns):
    active_ret = portfolio_returns - benchmark_returns
    return np.mean(active_ret) / np.std(active_ret)

def beta(portfolio_returns, benchmark_returns):
    benchmark_returns = benchmark_returns.loc[portfolio_returns.index[0]:portfolio_returns.index[-1]]
    joint = np.vstack([portfolio_returns.values, benchmark_returns.values])
    cov = np.cov(joint, ddof=0)
    if np.absolute(cov[1, 1]) < 1.0e-30:
        return np.nan
    return cov[0, 1] / cov[1, 1]

def alpha(portfolio_returns, benchmark_returns, risk_free_rate, ann_factor):
    ann_portfolio_ret = ann_factor * np.mean(portfolio_returns)
    ann_benchmark_ret = ann_factor * np.mean(benchmark_returns)
    b = beta(portfolio_returns, benchmark_returns)
    return ann_portfolio_ret - risk_free_rate - (b * ann_benchmark_ret)

def treynor_ratio(portfolio_returns, benchmark_returns, risk_free_rate, ann_factor):
    ann_portfolio_ret = ann_factor * np.mean(portfolio_returns)
    b = beta(portfolio_returns, benchmark_returns)
    return (ann_portfolio_ret - risk_free_rate) / b

def max_drawdown(returns):
    cum_ret = (1 + returns).cumprod()
    max_ret = np.fmax.accumulate(cum_ret)
    return np.nanmin((cum_ret - max_ret) / max_ret)
