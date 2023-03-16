from pprint import pformat
from typing import Dict, Union

import requests
from deepdiff import DeepDiff
from requests import RequestException

from .build_helpers import validate_cfg_object
from ..networking import wled_http_api
from src.networking.web_utils import get_host
from src.utils.json_utils import json_str_file_or_object, resolve_json_to_object


def upload_cfg_json(mdns_or_ip, x: json_str_file_or_object):
    return wled_http_api.post_json_via_edit_route(mdns_or_ip, x, "/cfg.json", validate_cfg_object)

    #### regular post to /json/cfg.json - DIDNT WORK!! (got 200 but led settings reset each time, maybe others.)
    # loaded_obj = resolve_json_to_object(x)
    # validate_cfg_object(loaded_obj)
    #
    # route = '/json/cfg.json'
    #
    # print(f"Uploading cfg.json")
    # res = http_api.wled_post(mdns_or_ip, route, loaded_obj)
    # return res.ok


def upload_to_wled_ap(cfg_json: json_str_file_or_object, mdns_name: str):
    ip = "4.3.2.1"
    print(f"local ({ip}) uploading: {mdns_name}")
    upload_cfg_json(ip, cfg_json)


def upload_cfg_files(mdns_to_files_map: Dict[str, str], reboot_after_upload=False):
    """Upload the map cfg_json filepaths to WLED.
    :returns a list of failed uploads. empty list if none.
    """
    failed_uploads = []
    for name in mdns_to_files_map:
        try:
            success = upload_cfg_json(name, mdns_to_files_map[name])
            if success and reboot_after_upload:
                wled_http_api.send_reboot_request(name)
            if not success:
                failed_uploads.append(name)
        except Exception as e:
            print(f'Unhandled {type(e).__name__} in uploading! ({name}): {e}')
            failed_uploads.append(name)

    return failed_uploads


def verify_test_live_panels(mdns_to_files_map: Dict[str, str]):
    print("Testing live panels...")
    fails_to_reasons_dict: Dict[str, str] = {}

    def add_http_error(url: str, response_or_error: Union[requests.Response, Exception]):
        error_str = f"HTTP Error {url}. "
        is_response = isinstance(response_or_error, requests.Response)
        reason = f"[{response_or_error.status_code} {response_or_error.reason}]" if is_response else repr(
            response_or_error)
        fails_to_reasons_dict[mdns] = error_str + reason

    for mdns in mdns_to_files_map:
        host = get_host(mdns)
        url = f"http://{host}/json/cfg.json"

        print(f"Testing {mdns}:")
        print(f"\t GET {url}... ", end="")
        try:
            # simple test - get cfg.json (is instance even online?)
            json_response = requests.get(url)
            print(json_response.status_code)
            if json_response.ok:
                # cfg.json test - same as expected?
                print("\t Compare JSON to expected: ", end='')
                actual = json_response.json()
                expected = resolve_json_to_object(mdns_to_files_map[mdns])
                diff = DeepDiff(actual, expected)

                print("match OK" if not diff else "JSON MISMATCH!")
                if diff:
                    fails_to_reasons_dict[mdns] = f"cfg.json mismatch: \n\t{pformat(diff, indent=2)}"

            else:
                print()
                add_http_error(url, json_response)

        except RequestException as e:
            add_http_error(url, e)
            continue

        DEFAULT_COLOR = (255, 160, 0)

        print("\tSetting test colors (default, r, g, b)...", end='')
        try:
            colors_json_res = wled_http_api.set_state(mdns, {
                "on": True,
                "transition": 7,
                "seg": [
                    {"col": [DEFAULT_COLOR]},
                    {"col": [(255, 0, 0)]},
                    {"col": [(0, 255, 0)]},
                    {"col": [(0, 0, 255)]},
                ]
            })
            print("OK" if colors_json_res else '???')
        except RequestException as e:
            add_http_error(url, e)
            continue

    num_errors = len(fails_to_reasons_dict)
    print(f"HTTP Verification Finished", end='')
    if num_errors:
        print(f"PROBLEMS FOUND: {num_errors}")
        for mdns in fails_to_reasons_dict:
            print(f"\t{mdns}: {fails_to_reasons_dict[mdns]}")
    else:
        print(" OK!")
    print()
