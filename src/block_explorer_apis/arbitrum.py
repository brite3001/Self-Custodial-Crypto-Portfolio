from . import request_helper
from . import colour_logs
from json.decoder import JSONDecodeError

logs = colour_logs.get_colour_logs()


def get_arbiscan_tokens(config: dict) -> dict:
    api_key = config["api_keys"]["arbitrum"]
    address = config["addresses"]["arbitrum"]
    whitelist = config["arbitrum_Whitelist"]

    tokens = {}
    for token_name, token_contract in whitelist.items():
        api_url = f"https://api.arbiscan.io/api?module=account&action=tokenbalance&contractaddress={token_contract}&address={address}&tag=latest&apikey={api_key}"

        response = request_helper.make_http_request(url=api_url, session=True)

        try:
            data = response.json()
            tokens[token_name] = (
                int(data["result"]) / (10**18)
                if token_name != "Wrapped BTC"
                else int(data["result"]) / (10**8)
            )

        except JSONDecodeError as json_err:
            logs.error(json_err)
            raise json_err

    return tokens
