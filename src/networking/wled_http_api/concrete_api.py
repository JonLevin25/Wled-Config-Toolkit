from .generic_api import *


# todo: extract decorators?
def get_state(mdns_or_ip: str):
    return wled_get(mdns_or_ip, '/json/state')


# reboot doesnt work so well... at least immediately after config.
def send_reboot_request(mdns_or_ip: str):
    wled_post(mdns_or_ip, '/json/', {'rb': True})


def set_state(mdns_or_ip: str, json_or_object):
    host = get_host(mdns_or_ip)
    url = f'http://{host}/json/state'
    val = content_to_json_str(json_or_object)

    if val is None:
        return
    res = requests.post(url, val)
    return res.json()


def get_info(mdns_or_ip: str):
    return wled_get(mdns_or_ip, '/json/info')


# todo: extract decorators
def get_effects(mdns_or_ip: str):
    return wled_get(mdns_or_ip, '/json/eff')


def get_palettes(mdns_or_ip: str):
    return wled_get(mdns_or_ip, '/json/pal')
