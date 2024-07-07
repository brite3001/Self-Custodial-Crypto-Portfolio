from json.decoder import JSONDecodeError
from . import request_helper
from . import colour_logs

logs = colour_logs.get_colour_logs()


def get_bitcoin_balance(config: dict) -> dict:
    address = config["addresses"]["bitcoin"]
    api_url = f"https://blockchain.info/rawaddr/{address}"

    response = request_helper.make_http_request(url=api_url, session=False)

    tokens = {}

    try:
        data = response.json()

        # Retrieve the balance from the response data.
        tokens["Bitcoin"] = data["final_balance"] / 10**8

    except JSONDecodeError as json_err:
        logs.error(json_err)
        raise json_err

    return tokens
