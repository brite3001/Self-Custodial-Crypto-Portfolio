from attrs import define, validators, field

from .token_objects import EthereumToken, OptimismToken
from .token_template import TokenTemplate


@define
class Portfolio:
    config: dict = field(validator=[validators.instance_of(dict)])
    tokens: list[TokenTemplate] = []

    portfolio_value: float = 0

    blockchain_mapping: dict = {
        "ethereum": EthereumToken,
        "optimism": OptimismToken,
    }

    got_balances: bool = False
    got_prices: bool = False
    got_actual_allocation: bool = False
    got_allocation_delta: bool = False

    def __attrs_post_init__(self):
        self.init_portfolio()

    def init_portfolio(self):
        allocations = self.config["allocations"]
        for name, info in self.config["tokens"].items():
            token = None

            if info["blockchain"] in self.blockchain_mapping:
                token = self.blockchain_mapping[info["blockchain"]](
                    name=name,
                    coingecko_name=info["coingecko_name"],
                    token_address=self.config["addresses"][info["blockchain"]],
                    contract_address=info["contract_address"],
                    decimals=info["decimals"],
                    api_key=self.config["api_keys"][info["blockchain"]],
                    allocation=allocations[name],
                )
            else:
                print(f"Blockchain {info['blockchain']} hasnt been implemented yet")

            if token is not None:
                self.tokens.append(token)
            else:
                print(f"Token {name} not added")

    def get_token_balances(self):
        for token in self.tokens:
            token.get_balance()

        self.got_balances = True

    def get_token_prices(self):
        for token in self.tokens:
            token.get_price()

        self.got_prices = True

    def calculate_portfolio_value(self):
        assert self.got_balances
        assert self.got_prices
        total_value = 0
        for token in self.tokens:
            total_value += token.balance * token.price

        self.portfolio_value = total_value

    def calculate_actual_token_allocation(self):
        assert self.portfolio_value > 0
        assert self.got_balances
        assert self.got_prices
        for token in self.tokens:
            token.actual_allocation = (
                (token.price * token.balance) / self.portfolio_value
            ) * 100

        self.got_actual_allocation = True

    def calculate_missing_allocations(self):
        allocation = 100
        tokens_without_allocation = 0

        for token in self.tokens:
            if token.allocation > 0:
                allocation -= token.allocation
            else:
                tokens_without_allocation += 1

        allocation /= tokens_without_allocation

        for token in self.tokens:
            if token.allocation == 0:
                token.allocation = allocation

    def calculate_allocation_delta(self):
        assert self.portfolio_value > 0
        assert self.got_balances
        assert self.got_prices
        assert self.got_actual_allocation
        for token in self.tokens:
            token.allocation_delta = (token.allocation - token.actual_allocation) / 100

        self.got_allocation_delta = True

    def generate_balancing_advice(self):
        assert self.portfolio_value > 0
        assert self.got_balances
        assert self.got_prices
        assert self.got_actual_allocation
        assert self.got_allocation_delta

        for token in self.tokens:
            delta_in_usd = token.allocation_delta * self.portfolio_value
            if token.allocation_delta > 0:
                print(
                    f"BUY ${delta_in_usd} ({delta_in_usd / token.price}) worth of {token.name} (delta = {token.allocation_delta})"
                )
            else:
                print(
                    f"SELL ${delta_in_usd} ({-(delta_in_usd / token.price)}) worth of {token.name} (delta = {token.allocation_delta})"
                )
