from attrs import define, validators, field
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt

from .token_objects import (
    EthereumToken,
    OptimismToken,
    AlgorandToken,
    ArbitrumToken,
    BitcoinToken,
    DecredToken,
    FluxToken,
    PolygonToken,
    SolanaToken,
    WaxToken,
    MoneroToken,
    BeamToken,
    InternetComputerToken,
    MinaProtocolToken,
    NeonEVMToken,
    Ethereum,
    HoirzenToken,
    EnjinCoinToken,
    FiroToken,
)
from .token_template import TokenTemplate

cg = CoinGeckoAPI()


@define
class Portfolio:
    config: dict = field(validator=[validators.instance_of(dict)])
    tokens: list[TokenTemplate] = field(factory=list)

    portfolio_value: float = 0

    blockchain_mapping: dict = {
        "ethereum": EthereumToken,
        "optimism": OptimismToken,
        "algorand": AlgorandToken,
        "arbitrum": ArbitrumToken,
        "bitcoin": BitcoinToken,
        "decred": DecredToken,
        "flux": FluxToken,
        "polygon": PolygonToken,
        "solana": SolanaToken,
        "wax": WaxToken,
        "monero": MoneroToken,
        "beam": BeamToken,
        "internet_computer": InternetComputerToken,
        "mina_protocol": MinaProtocolToken,
        "neon_evm": NeonEVMToken,
        "eth": Ethereum,
        "horizen": HoirzenToken,
        "enjin_coin": EnjinCoinToken,
        "firo": FiroToken,
    }

    got_balances: bool = False
    got_prices: bool = False
    got_actual_allocation: bool = False
    got_allocation_delta: bool = False

    def __attrs_post_init__(self):
        self.init_portfolio()

    def init_portfolio(self):
        allocations = self.config["allocations"]
        api_key = ""
        for name, info in self.config["tokens"].items():
            token = None

            if info["blockchain"] in self.blockchain_mapping:
                if info["blockchain"] in self.config["api_keys"]:
                    api_key = self.config["api_keys"][info["blockchain"]]

                token = self.blockchain_mapping[info["blockchain"]](
                    name=name,
                    coingecko_name=info["coingecko_name"],
                    token_address=self.config["addresses"][info["blockchain"]],
                    contract_address=info["contract_address"],
                    decimals=info["decimals"],
                    api_key=api_key,
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
        tokens_pending_prices = []
        for token in self.tokens:
            tokens_pending_prices.append(token.coingecko_name)

        p = cg.get_price(
            ids=tokens_pending_prices,
            vs_currencies="usd",
        )

        for coingecko_name, price in p.items():
            for token in self.tokens:
                if token.coingecko_name == coingecko_name:
                    token.price = price["usd"]

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

        sorted_smallest = sorted(self.tokens, key=lambda x: x.allocation_delta)

        for token in sorted_smallest[:5] + sorted_smallest[-5:]:
            delta_in_usd = token.allocation_delta * self.portfolio_value
            if token.allocation_delta > 0:
                print(
                    f"BUY ${delta_in_usd} ({delta_in_usd / token.price}) worth of {token.name} (delta = {token.allocation_delta})"
                )
            else:
                print(
                    f"SELL ${delta_in_usd} ({-(delta_in_usd / token.price)}) worth of {token.name} (delta = {token.allocation_delta})"
                )

    def pie_chart(self):
        assert self.portfolio_value > 0
        assert self.got_balances
        assert self.got_prices
        assert self.got_actual_allocation
        assert self.got_allocation_delta

        labels = []
        target_percentages = []
        current_percentages = []

        for token in self.tokens:
            labels.append(token.name)
            target_percentages.append(token.allocation)
            current_percentages.append(token.actual_allocation)

        fig, (ax1, ax2) = plt.subplots(ncols=2)
        ax1.pie(target_percentages, labels=labels, autopct="%.2f%%")
        ax1.set_title("Target Allocations")

        ax2.pie(current_percentages, labels=labels, autopct="%.2f%%")
        ax2.set_title("Current Allocations")

        plt.show()
