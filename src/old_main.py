from block_explorer_apis import (
    arbitrum,
    polygon,
    optimism,
    ethereum,
    solana,
    algorand,
    bitcoin,
    flux,
    wax,
)

import coingecko

import yaml
import pandas as pd
import matplotlib.pyplot as plt
from block_explorer_apis.colour_logs import get_colour_logs

logs = get_colour_logs()


# Stop long balances from being truncated
pd.options.display.precision = 16
# pd.options.display.max_columns = 20
# pd.set_option("display.max_colwidth", 100)


def main():
    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    allocations = config["allocations"]

    # Here we use the helper functions to populate the token balances for each coin
    # across all the different supported networks.
    networks = {
        "Arbitrum": arbitrum.get_arbiscan_tokens(config),
        "Polygon": polygon.get_polygon_tokens(config),
        "Optimism": optimism.get_optimism_tokens(config),
        "Ethereum": ethereum.get_ethereum_tokens(config),
        "Solana": solana.get_solana_balance(config),
        "Algorand": algorand.get_algorand_balance(config),
        "Bitcoin": bitcoin.get_bitcoin_balance(config),
        "Flux": flux.get_flux_balance(config),
        "Wax": wax.get_wax_balance(config),
        "Monero": {"Monero": 52},
        "Beam": {"Beam": 8253},
        "Internet Computer": {"Internet Computer": 159},
        # Add support for
        # NEON EVM (phantom browser wallet)
        # Mina Protocol (auro browser wallet)
        # Add a staking balance to the portfolio (non-tradable part of portfolio)
        # OOP rewrite
    }

    tokens = []

    # Here we're making a list to feed into a dataframe.
    # We iterate through each network, extract the tokens(s) from each network
    # then make each token its own dictionary, before adding it to the list.
    for network, network_tokens in networks.items():
        for token, balance in network_tokens.items():
            tokens.append(
                {
                    "token": token,
                    "balance": balance,
                    "network": network,
                    "target_%": allocations[token],
                }
            )

    df = pd.DataFrame(tokens)

    # If I want to specify a few allocations for some particlar tokens e.g.
    # just Bitcoin and XMR, I can allocate the remaining part of the portfolio
    # equally for the remaining assets.
    # allocation_adjustment = df["target_%"].isin([0]).any()

    # if allocation_adjustment:
    #     unallocated_tokens = df["target_%"].value_counts()[0]
    #     print(
    #         f"{unallocated_tokens} tokens require their allocation(s) to be calculated"
    #     )
    #     remaining_allocation = 100 - df["target_%"].sum()
    #     print(f"remaining: {remaining_allocation}%")
    #     allocation_per_token = round(remaining_allocation / unallocated_tokens, 4)
    #     print(
    #         f"Allocating {allocation_per_token}% for remaining {unallocated_tokens} tokens"
    #     )

    #     df["target_%"].replace(0, allocation_per_token, inplace=True)

    # coin_gecko_prices = coingecko.get_prices(df["token"].to_list())

    # print(coin_gecko_prices)

    # # Check for missing prices in coin data
    # missing_coins = []
    # for token_name in df["token"].to_list():
    #     if token_name not in coin_gecko_prices.keys():
    #         missing_coins.append(token_name)

    # if len(missing_coins) == 0:
    #     print("No missing coins, price data good!")
    # else:
    #     print("Coins missing from price data!")
    #     print(missing_coins)

    # # Add new price data to the df
    # for index, row in df.iterrows():
    #     df.at[index, "price"] = coin_gecko_prices[row["token"]]

    # Calculate current portfolio value in USD
    portfolio_value = (df["balance"] * df["price"]).sum()
    print(portfolio_value)

    # Calculate the current percentage allocation of each coin
    df["current_%"] = ((df["balance"] * df["price"]) / float(portfolio_value)) * 100

    # Calculate the difference between the target_% and current_%
    df["delta"] = df["target_%"] - df["current_%"]

    # Order the df by largest delta
    top_five_delta = df.loc[df["delta"].abs().nlargest(8).index]

    print(top_five_delta)

    # Print the advice for each token, should we buy or sell?
    for index, row in top_five_delta.iterrows():
        amount = (abs((row["delta"]) / 100) * portfolio_value) / row["price"]
        if row["delta"] < 0:
            print(
                f'SELL {amount} {row["token"]} on {row["network"]} (${amount * row["price"]})'
            )
        else:
            print(
                f'BUY {amount} {row["token"]} on {row["network"]} (${amount * row["price"]})'
            )

    # Here we print target portfolio, and compare it to our actual portfolio
    labels = []
    target_percentages = []
    current_percentages = []

    for index, row in df.iterrows():
        labels.append(row["token"])
        target_percentages.append(row["target_%"])
        current_percentages.append(row["current_%"])

    fig, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.pie(target_percentages, labels=labels, autopct="%.2f%%")
    ax1.set_title("Target Allocations")

    ax2.pie(current_percentages, labels=labels, autopct="%.2f%%")
    ax2.set_title("Current Allocations")

    plt.show()


if __name__ == "__main__":
    main()
