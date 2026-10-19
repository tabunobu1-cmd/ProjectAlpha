def momentum(prices, lookback=60):
    return prices / prices.shift(lookback) - 1.0

def forward_return(prices, horizon=20):
    return prices.shift(-horizon) / prices - 1.0
