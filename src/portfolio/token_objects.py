from json import JSONDecodeError
from attrs import define
import requests

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


@define
class ArbitrumToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://api.arbiscan.io/api?module=account&action=tokenbalance&contractaddress={self.contract_address}&address={self.token_address}&tag=latest&apikey={self.api_key}"

        response = make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            self.balance = float(data["result"]) / 10**self.decimals
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class PolygonToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={self.contract_address}&address={self.token_address}&tag=latest&apikey={self.api_key}"

        response = make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            self.balance = float(data["result"]) / 10**self.decimals
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class AlgorandToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://mainnet-api.algonode.cloud/v2/accounts/{self.token_address}"
        # https://editor.swagger.io/?url=https://openapi.algonode.cloud/algod.oas3.json

        response = make_http_request(url=api_url, session=False)

        try:
            data = response.json()
            self.balance = float(data["amount"] / 10**self.decimals)
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class BitcoinToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://blockchain.info/rawaddr/{self.token_address}"

        response = make_http_request(url=api_url, session=False)

        try:
            data = response.json()
            self.balance = float(data["final_balance"] / 10**self.decimals)
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class DecredToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://dcrdata.decred.org/api/address/{self.token_address}/totals"

        response = make_http_request(url=api_url, session=False)

        try:
            data = response.json()
            self.balance = float(data["dcr_unspent"])
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class FluxToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://api.runonflux.io/explorer/balance/{self.token_address}"

        response = make_http_request(url=api_url, session=False)

        try:
            data = response.json()
            self.balance = float(data["data"] / 10**self.decimals)
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class MinaProtocolToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = f"https://api.minaexplorer.com/accounts/{self.token_address}"

        response = make_http_request(url=api_url, session=False)

        try:
            data = response.json()
            self.balance = float(data["account"]["balance"]["total"])

        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class FiroToken(TokenTemplate):
    # https://github.com/firoorg/insight-api-firo
    def get_balance(self) -> None:
        api_url = f"https://explorer.firo.org/insight-api-zcoin/addr/{self.token_address}/balance"

        response = make_http_request(url=api_url, session=False)

        try:
            data = response.json()
            print(data)
            self.balance = float(data / 10**self.decimals)

        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class EnjinCoinToken(TokenTemplate):
    def get_balance(self) -> None:
        url = "https://matrix.api.subscan.io/api/scan/account/tokens"
        headers = {
            "Content-Type": "application/json",
            # 'X-API-Key': api_key
        }
        payload = {"address": self.token_address}

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.balance = (
                    int(data["data"]["native"][0]["balance"]) / 10**self.decimals
                )
            else:
                print(
                    f"Failed to retrieve balance. Status code: {response.status_code}"
                )
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching balance: {e}")
            return None


@define
class WaxToken(TokenTemplate):
    def get_balance(self) -> None:
        api_url = "https://api.wax.alohaeos.com/v1/chain/get_account"
        params = {"account_name": self.token_address}

        try:
            response = requests.post(api_url, json=params)
            data = response.json()
            balance = data["core_liquid_balance"]
            self.balance = float(balance.replace("WAX", "").replace(" ", ""))
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err


@define
class SolanaToken(TokenTemplate):
    def get_balance(self) -> None:
        rpc_url = "https://api.mainnet-beta.solana.com/"

        payload = {}

        # Query for Solana
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [self.token_address],
        }

        try:
            response = requests.post(rpc_url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.balance = float(data["result"]["value"] / 10**9)

        except JSONDecodeError as json_err:
            logs.error(json_err)


@define
class MoneroToken(TokenTemplate):
    def get_balance(self) -> None:
        self.balance = 45.87


@define
class BeamToken(TokenTemplate):
    def get_balance(self) -> None:
        self.balance = 14510


@define
class InternetComputerToken(TokenTemplate):
    def get_balance(self) -> None:
        self.balance = 159.0


@define
class NeonEVMToken(TokenTemplate):
    def get_balance(self) -> None:
        self.balance = 1043


@define
class HoirzenToken(TokenTemplate):
    def get_balance(self) -> None:
        self.balance = 512.0


@define
class Ethereum(TokenTemplate):
    def get_balance(self) -> None:
        self.balance = 36.5
