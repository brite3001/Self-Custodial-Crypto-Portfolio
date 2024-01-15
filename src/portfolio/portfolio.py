from attrs import define, validators, field

from .token_objects import EthereumToken, OptimismToken


@define
class Portfolio:
    config: dict = field(validator=[validators.instance_of(dict)])
    tokens: list = []

    blockchain_mapping: dict = {
        "ethereum": EthereumToken,
        "optimism": OptimismToken,
    }

    def __attrs_post_init__(self):
        self.init_portfolio()

    def init_portfolio(self):
        for token_name, info in self.config["tokens"].items():
            print(token_name)
            print(info)

            token = None

            if info["blockchain"] in self.blockchain_mapping:
                token = self.blockchain_mapping[info["blockchain"]](
                    token_name=token_name,
                    coingecko_name=info["coingecko_name"],
                    token_address=self.config["addresses"]["ethereum"],
                    contract_address=info["contract_address"],
                    decimals=info["decimals"],
                    api_key=self.config["api_keys"]["ethereum"],
                )
            else:
                print(f"Blockchain {info['blockchain']} hasnt been implemented yet")

            if token is not None:
                self.tokens.append(token)
            else:
                print(f"Token {token_name} not added")

    def calculate_missing_allocations(self):
        allocation = 100

        for token in self.tokens:
            if token.allocation > 0:
                allocation -= token.allocation

        print(f"remaining allocation = {allocation}")
