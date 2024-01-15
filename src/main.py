from portfolio.portfolio import Portfolio
import yaml


def main():
    p = Portfolio

    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
        p = Portfolio(config=config)

    print(p.tokens)

    # allocations = config["allocations"]

    # for token in tokens:
    #     # token.get_balance()
    #     # token.get_price()

    #     if token.token_name in allocations:
    #         token.allocation = allocations[token.token_name]

    # p.calculate_missing_allocations()


if __name__ == "__main__":
    main()
