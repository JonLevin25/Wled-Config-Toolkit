import ipaddress
import json

from src.utils.json_override import resolve_json_to_object
from .mdns_resolver import resolve_mdns


def get_host(mdns_or_ip: str) -> str:
    try:
        ipaddress.ip_address(mdns_or_ip)
    except ValueError:
        resolved = resolve_mdns(mdns_or_ip)
        if resolved:
            return resolved
        if not mdns_or_ip.endswith('.local'):
            return mdns_or_ip + '.local'
    return mdns_or_ip


def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def content_to_json_str(json_or_object):
    if type(json_or_object) == str:
        try:
            json.loads(json_or_object)
            return json_or_object
        except json.decoder.JSONDecodeError:
            print("ERROR: Bad json!")
            return None
    if type(json_or_object) != dict:
        print("ERROR: expecting dict to convert to json..")
        return None
    return json.dumps(json_or_object)


def are_base_properties_same(json_or_object: json):
    resolve_json_to_object(json_or_object)
