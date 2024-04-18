from portfolio.portfolio import Portfolio
import yaml

# TODO: Bundle the API calls with sessions for blockchain explorers
# ~~ TODO: Make 1 API call to coingecko to get all the price data ~~
# TODO: Modify balancing_advice by adding buy/sell matching functionality to swap tokens, rather than vague BUY or SELL advice.
# TODO: use rich https://github.com/Textualize/rich for more pretty terminal output
# TODO: progress bars -> use rich
# TODO: A while true loop to make the program more interactive
# TODO: A TUI using rich?
# TODO: Graphing in the terminal? https://github.com/kroitor/asciichart https://github.com/Textualize/rich/discussions/1002#discussioncomment-424554


def main():
    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
        p = Portfolio(config=config)

    p.get_token_balances()
    p.get_token_prices()

    for token in p.tokens:
        print(f"{token.name} | {token.balance} | {token.price}")

    p.calculate_missing_allocations()

    for token in p.tokens:
        print(f"{token.name} | {token.allocation}%")

    p.calculate_portfolio_value()
    print(p.portfolio_value)

    p.calculate_actual_token_allocation()

    p.calculate_allocation_delta()

    p.generate_balancing_advice()


if __name__ == "__main__":
    main()
