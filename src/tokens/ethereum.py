from pycoingecko import CoinGeckoAPI
from json import JSONDecodeError
from attrs import define, field, validators
from .request_helper import make_http_request
from .colour_logs import get_colour_logs

logs = get_colour_logs()
cg = CoinGeckoAPI()


@define
class EthereumToken:
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

    def get_balance(self) -> None:
        api_url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={self.contract_address}&address={self.token_address}&tag=latest&apikey={self.api_key}"

        response = make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            self.balance = float(data["result"]) / 10**self.decimals
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err

    def get_price(self) -> None:
        p = cg.get_price(
            ids=self.coingecko_name if self.coingecko_name != "" else self.token_name,
            vs_currencies="usd",
        )

        for _, price in p.items():
            self.price = price["usd"]
