from attrs import define, validators, field
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


@define
class TokenTemplate:
    token_name: str = field(validator=[validators.instance_of(str)])
    coingecko_name: str = field(
        validator=[validators.instance_of(str)]
    )  # some tokens have slightly different names in the coingecko API

    token_address: str = field(validator=[validators.instance_of(str)])
    contract_address: str = field(validator=[validators.instance_of(str)])
    decimals: int = field(validator=[validators.instance_of(int)])
    api_key: str = field(validator=[validators.instance_of(str)])

    allocation: float = field(init=False)  # allocation % in portfolio
    price: float = field(init=False)  # current price of token according to coingecko
    balance: float = field(init=False)  # balance in token_address

    def get_price(self) -> None:
        p = cg.get_price(
            ids=self.coingecko_name if self.coingecko_name != "" else self.token_name,
            vs_currencies="usd",
        )

        for _, price in p.items():
            self.price = price["usd"]
