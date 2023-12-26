from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

translations = {
    "Aave (PoS)": "aave",
    "Synthetix Network Token (PoS)": "havven",
    "PYR Token": "vulcan-forged",
    "LoopringCoin V2": "loopring",
    "Axie Infinity Shard": "axie-infinity",
    "Wrapped BTC": "wrapped-btc-trustless-bridge",
    "OMG Network": "omisego",
    "Immutable X": "immutable-x",
    "Flux": "zelcash",
    "Internet Computer": "internet-computer",
}


def translate_token_name(tokens: list) -> list:
    """
    Some of the layer 2 networks have different names for their tokens.
    Here we'll change the names so they're compatible with the coingecko API
    Also coingecko has old or weird names for same tokens too....

    Args:
        tokens (list): token list from the portfolio_balancer

    Returns:
        list: token list with coingecko friendly names
    """

    for old_token_name, coin_gecko_token_name in translations.items():
        if old_token_name in tokens:
            tokens.remove(old_token_name)
            tokens.append(coin_gecko_token_name)

    return tokens


def reverse_translation(tokens: dict) -> dict:
    """
    Converts the coingecko token names back to the original token names.
    Also do some name correction to match original portfolio_balancer.py names.

    Args:
        tokens (dict): price dict from coingecko

    Returns:
        dict: the original token names, with the nested price dictionaries from coingecko flattened
    """

    for old_token_name, coin_gecko_token_name in translations.items():
        if coin_gecko_token_name in tokens:
            tokens[old_token_name] = tokens[coin_gecko_token_name]["usd"]
            del tokens[coin_gecko_token_name]

    # Fix the capitalisation
    for token_name, price in tokens.items():
        if not token_name.istitle():
            tokens[token_name.title()] = price
            del tokens[token_name]

    # Flatten remaining price dicts
    for token_name, price in tokens.items():
        if isinstance(price, dict):
            tokens[token_name] = tokens[token_name]["usd"]

    # Fix unique token names
    unique_names = {
        "(Pos) Wrapped Btc": "(PoS) Wrapped BTC",
        "Enjincoin": "EnjinCoin",
        "Aave (Pos)": "Aave (PoS)",
        "Gmx": "GMX",
        "uniswap": "Uniswap",
        "wax": "Wax",
    }

    for wrong_token_format, correct_token_format in unique_names.items():
        if wrong_token_format in tokens:
            tokens[correct_token_format] = tokens[wrong_token_format]
            del tokens[wrong_token_format]

    return tokens


def get_prices(tokens: list) -> dict:
    tokens = translate_token_name(tokens)
    polygon_bitcoin = True if "(PoS) Wrapped BTC" in tokens else False

    prices = cg.get_price(ids=tokens, vs_currencies="usd")

    if polygon_bitcoin:
        prices["(PoS) Wrapped BTC"] = prices["bitcoin"]

    prices_translated = reverse_translation(prices)

    return prices_translated


# print(cg.get_price(ids="internet-computer", vs_currencies="usd"))
# print(cg.search("Internet Computer"))
