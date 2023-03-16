from typing import Any, Callable, Dict

from pprint import pprint
import requests
from src.networking.web_utils import *
from src.utils.json_utils import json_str_file_or_object


def wled_get(mdns_or_ip: str, route: str):
    host = get_host(mdns_or_ip)
    url = f'http://{host}{route}'
    response = requests.get(url)
    result = response.json()
    pprint(result)
    return result


def wled_post(mdns_or_ip: str, route: str, content_json: Any):
    host = get_host(mdns_or_ip)
    url = f'http://{host}{route}'
    resolved_json = resolve_json_to_object(content_json)

    print(f'POST {url}... ', end='')
    response = requests.post(url, json=resolved_json)  # requests expects the actual object, and serializes it itself.
    print(f'{response.status_code} {response.reason}')
    pprint(response.json())
    return response


def get_wled_file_via_edit_route(mdns_or_ip: str, filename: str = 'cfg.json'):
    host = get_host(mdns_or_ip)
    url = f'http://{host}/edit?edit=/{filename}'
    print(f'getting url: {url}... ', end='')
    res = requests.get(url)
    if res.ok:
        print(f" OK! [{res.status_code}]")
        return res.json()
    else:
        print(f" ~~ FAILED! ~~ [{res.status_code}]")
        return None


def post_json_via_edit_route(mdns_or_ip, cfg_json: json_str_file_or_object, filename: str = "/cfg.json",
                             validate_fn: Callable[[Dict], None] = None):
    if not filename.startswith('/'):
        print(f'expected config filename to start with forward slash. adding.')
        filename = '/' + filename

    host = get_host(mdns_or_ip)
    url = f'http://{host}/edit'

    # get the config object, validate it, and serialize
    loaded_obj = resolve_json_to_object(cfg_json)
    if validate_fn:
        validate_fn(loaded_obj)
    json_str = json.dumps(loaded_obj)

    print(f"Uploading cfg.json to {url}...", end='')
    res = requests.post(url, files={'data': (filename, json_str, 'text/json')})
    if res.ok:
        print(f" OK! [{res.status_code}] {res.text}")
        return True
    else:
        print(f" ~~ FAILED! ~~ [{res.status_code}] {res.text}")
        return False
