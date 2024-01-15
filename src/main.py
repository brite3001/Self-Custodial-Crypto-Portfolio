from tokens.ethereum import EthereumToken
import yaml


def main():
    tokens = []

    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

        for token_name, info in config["ethereum_tokens"].items():
            print(token_name)
            print(info)

            tokens.append(
                EthereumToken(
                    token_name=token_name,
                    coingecko_name=info["coingecko_name"],
                    token_address=config["addresses"]["ethereum"],
                    contract_address=info["contract_address"],
                    decimals=info["decimals"],
                    api_key=config["api_keys"]["ethereum"],
                )
            )

    for x in tokens:
        x.get_balance()

    for x in tokens:
        x.get_price()

    for x in tokens:
        print(x)
        print("\n")


if __name__ == "__main__":
    main()
