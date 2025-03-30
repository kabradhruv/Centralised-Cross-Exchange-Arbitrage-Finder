from django.shortcuts import render
import ccxt
from django.http import JsonResponse

# Initialize exchange instances
exchanges = {
    "Binance": ccxt.binance(),
    "Kraken": ccxt.kraken(),
    "Coinbase": ccxt.coinbase(),
    "Bitfinex": ccxt.bitfinex()
}

# List of cryptocurrency pairs to track (10 pairs)
CRYPTO_PAIRS = [
    "BTC/USDT", "ETH/USDT", "ADA/USDT", "XRP/USDT", "SOL/USDT",
    "DOGE/USDT", "DOT/USDT", "LTC/USDT", "BCH/USDT", "LINK/USDT"
]

# Define the minimum profit threshold in percentage
PROFIT_THRESHOLD = 0.5

def fetch_prices():
    """
    Fetches bid/ask prices from multiple exchanges for selected crypto pairs.
    Computes arbitrage opportunities where profit is at least 10%.
    """
    results = []
    arbitrage_opportunities = []

    for pair in CRYPTO_PAIRS:
        pair_data = {"pair": pair, "prices": {}}

        # Get prices from each exchange for the current pair
        for ex_name, ex in exchanges.items():
            try:
                ticker = ex.fetch_ticker(pair)
                pair_data["prices"][ex_name] = {
                    "ask": ticker.get("ask"),
                    "bid": ticker.get("bid")
                }
            except Exception as e:
                pair_data["prices"][ex_name] = {
                    "ask": None,
                    "bid": None,
                    "error": str(e)
                }

        results.append(pair_data)

        # Compute arbitrage opportunities for any buy/sell combination
        for buy_ex, buy_data in pair_data["prices"].items():
            for sell_ex, sell_data in pair_data["prices"].items():
                if buy_ex == sell_ex:
                    continue
                # Ensure both ask and bid are available before calculating
                if buy_data.get("ask") and sell_data.get("bid"):
                    buy_price = buy_data["ask"]
                    sell_price = sell_data["bid"]
                    profit_pct = round(((sell_price - buy_price) / buy_price) * 100, 2)
                    if profit_pct >= PROFIT_THRESHOLD:
                        arbitrage_opportunities.append({
                            "pair": pair,
                            "buy_exchange": buy_ex,
                            "sell_exchange": sell_ex,
                            "buy_price": buy_price,
                            "sell_price": sell_price,
                            "profit_pct": profit_pct
                        })

    return {"prices": results, "arbitrage_opportunities": arbitrage_opportunities}

def dashboard(request):
    """Renders the dashboard template with exchanges context."""
    context = {
        "exchanges": ["Binance", "Kraken", "Coinbase", "Bitfinex"]
    }
    return render(request, "dashboard.html", context)

def get_prices(request):
    """API endpoint that returns updated price and arbitrage data as JSON."""
    data = fetch_prices()
    return JsonResponse(data)
