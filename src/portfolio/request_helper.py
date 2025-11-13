import requests
import time
from . import colour_logs

logs = colour_logs.get_colour_logs()


def make_http_request(url: str, session: bool, headers=None, max_retries=5):
    retries = 0

    while retries < max_retries:
        try:
            response = (
                requests.Session().get(url, headers=headers)
                if session
                else requests.get(url, headers=headers)
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            logs.error(http_err)
        except requests.exceptions.RequestException as req_err:
            logs.error(req_err)

        retries += 1
        if retries < max_retries:
            # Wait for a moment before retrying
            time.sleep(1)

    raise Exception("Something went wrong with one of the APIs... check the logs.")
