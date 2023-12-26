from json.decoder import JSONDecodeError
from . import request_helper
from . import colour_logs

logs = colour_logs.get_colour_logs()


# https://docs.runonflux.io/#tag/Explorer/operation/getAddressTransactions
def get_flux_balance(config: dict) -> dict:
    address = config["addresses"]["flux"]
    api_url = f"https://api.runonflux.io/explorer/balance/{address}"

    tokens = {}

    response = request_helper.make_http_request(url=api_url, session=False)

    try:
        data = response.json()
        tokens["Flux"] = data["data"] / 10**8
        return tokens
    except JSONDecodeError as json_err:
        logs.error(json_err)
        raise json_err
