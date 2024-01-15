from json import JSONDecodeError
from attrs import define

from .request_helper import make_http_request
from .colour_logs import get_colour_logs
from .token_template import TokenTemplate

logs = get_colour_logs()


@define
class EthereumToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={self.contract_address}&address={self.token_address}&tag=latest&apikey={self.api_key}"

        response = make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            self.balance = float(data["result"]) / 10**self.decimals
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class OptimismToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://api-optimistic.etherscan.io/api?module=account&action=tokenbalance&contractaddress={self.contract_address}&address={self.token_address}&tag=latest&apikey={self.api_key}"

        response = make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            self.balance = float(data["result"]) / 10**self.decimals
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err
