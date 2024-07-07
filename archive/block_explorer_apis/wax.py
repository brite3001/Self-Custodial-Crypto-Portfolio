import requests

from . import colour_logs

logs = colour_logs.get_colour_logs()


def get_wax_balance(config: dict) -> dict:
    address = config["addresses"]["wax"]
    api_url = "https://api.wax.alohaeos.com/v1/chain/get_account"
    params = {"account_name": address}

    tokens = {}

    try:
        response = requests.post(api_url, json=params)
        data = response.json()

        # Extract balance information from the response
        balance = data["core_liquid_balance"]
        tokens["Wax"] = float(balance.replace("WAX", "").replace(" ", ""))
        return tokens
    except Exception as e:
        print(f"Error: {e}")
        raise e
