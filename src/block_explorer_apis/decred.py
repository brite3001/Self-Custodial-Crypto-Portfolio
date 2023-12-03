from json.decoder import JSONDecodeError
from . import request_helper
from . import colour_logs

logs = colour_logs.get_colour_logs()


def get_decred_balance(config: dict) -> dict:
    address = config["addresses"]["decred"]
    api_url = f"https://dcrdata.decred.org/api/address/{address}/totals"

    tokens = {}

    response = request_helper.make_http_request(url=api_url, session=False)

    try:
        data = response.json()
        tokens["Decred"] = data["dcr_unspent"]
        return tokens
    except JSONDecodeError as json_err:
        logs.error(json_err)
        raise json_err
