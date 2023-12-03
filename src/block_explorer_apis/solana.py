import requests
import time
from json.decoder import JSONDecodeError
from . import colour_logs

logs = colour_logs.get_colour_logs()


def get_solana_balance(config: dict) -> dict:
    rpc_url = "https://api.mainnet-beta.solana.com/"
    address = config["addresses"]["solana"]

    tokens = {}

    # Create a JSON-RPC request to get the balance.
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address],
    }
    max_retries = 5

    retries = 0

    while retries < max_retries:
        try:
            response = requests.post(rpc_url, json=payload)
            response.raise_for_status()
            data = response.json()
            tokens["Solana"] = data["result"]["value"] / 10**9
            return tokens
        except requests.exceptions.HTTPError as http_err:
            logs.error(http_err)
        except requests.exceptions.RequestException as req_err:
            logs.error(req_err)
        except JSONDecodeError as json_err:
            logs.error(json_err)

        retries += 1
        if retries < max_retries:
            # Wait for a moment before retrying
            time.sleep(1)

    raise Exception("Something went wrong with the Solana API... check the logs.")
