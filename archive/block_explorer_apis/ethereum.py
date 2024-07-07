from json.decoder import JSONDecodeError
from . import request_helper
from . import colour_logs

logs = colour_logs.get_colour_logs()


def get_ethereum_tokens(config: dict) -> dict:
    api_key = config["api_keys"]["ethereum"]
    address = config["addresses"]["ethereum"]
    whitelist = config["ethereum_whitelist"]

    tokens = {}

    for token, contract in whitelist.items():
        api_url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract}&address={address}&tag=latest&apikey={api_key}"
        response = request_helper.make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            tokens[token] = int(data["result"]) / 10**18
        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err

    return tokens
