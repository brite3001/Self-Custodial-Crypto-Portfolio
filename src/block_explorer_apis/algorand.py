from json.decoder import JSONDecodeError
from . import request_helper
from . import colour_logs

logs = colour_logs.get_colour_logs()


# https://editor.swagger.io/?url=https://openapi.algonode.cloud/algod.oas3.json
def get_algorand_balance(config: dict) -> dict:
    address = config["addresses"]["algorand"]
    api_url = f"https://mainnet-api.algonode.cloud/v2/accounts/{address}"

    tokens = {}

    try:
        response = request_helper.make_http_request(url=api_url, session=False)
        data = response.json()
        tokens["Algorand"] = data["amount"] / 10**6

    except JSONDecodeError as json_err:
        logs.error(json_err)
        raise json_err

    return tokens
