

import requests

import utils.exceptions as excepts


def checkHttpCode(resp: requests.Response):
    if 200 <= resp.status_code < 300:
        return

    if 500 <= resp.status_code:
        raise excepts.DownException(
            f"status code {resp.status_code} on {resp.url}",
            resp.text)

    if 400 <= resp.status_code < 500:
        raise excepts.MumbleException(
            f"status code {resp.status_code} on {resp.url}",
            resp.text)

    raise excepts.DownException(
        f"unexpected behaviour on {resp.url}", resp.text)
