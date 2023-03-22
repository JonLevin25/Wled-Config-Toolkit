import os.path as path

from typing import List, Dict, Any, Tuple, Iterable, Union

from src.networking.web_utils import *
from src.utils.path_util import path_forced_root


def get_cfg_json_value_name_mdns(name: str) -> str:
    """
    will generate a json to override both "name" and "mdns" properties
    :param name:
    :return: json object
    """
    return json.dumps({
        'id': {
            'mdns': name,
            'name': name,
        }
    })


def extract_json_conf_data(conf_obj: Dict[str, Any], name: str, cfg_modules_dir: str) -> Tuple[List[str], Dict]:
    if name not in conf_obj:
        print(f'wled-conf file did not have {name} key.')
        return [], {}

    cfg = conf_obj[name]
    cfg_modules = [path_forced_root(cfg_modules_dir, t)
                   for t in cfg['cfg_modules']]
    overrides: Dict = cfg['overrides'] if 'overrides' in cfg else {}
    return cfg_modules, overrides


def get_mdns_names_from_conf(conf_file: str, cfgs_to_build: Union[str, Iterable[str]] = None) -> List[str]:
    loaded_conf = resolve_json_to_object(conf_file)
    if type(cfgs_to_build) == str:
        cfgs_to_build = [cfgs_to_build]  # ensure array-wrapped.

    def filter_mdns(mdns):
        if mdns == "$common":
            return False
        return not cfgs_to_build or mdns in cfgs_to_build

    # return all keys except $common. if relevant, filterr by overrides aswell
    return [mdns for mdns in loaded_conf if filter_mdns(mdns)]


def get_cfg_file_path(mdns_name: str, out_dir: str, renames_old_to_new: Dict[str, str] = None) -> str:
    """Get the path for cfg.json, given the mdns/IP.
    If rename is relevant, always return the 'new' name
    """
    renames_old_to_new = renames_old_to_new or {}
    # renames_new_to_old = {v: k for k, v in renames_old_to_new.items()}
    if mdns_name in renames_old_to_new:
        mdns_name = renames_old_to_new[mdns_name]
    return path.join(out_dir, f'cfg_{mdns_name}.json')


def validate_cfg_object(cfg_object: Dict):
    print("Validating generated config...")
    print("\tValidating basic structure... ", end="")
    assert all(prop in cfg_object for prop in ("hw", "nw", "ap", "wifi"))
    assert all(prop in cfg_object['hw'] for prop in ["led"])
    print("OK!")

    print("\tValidating WLED-AP has not been changed/removed... ", end="")
    assert cfg_object["ap"]["ssid"] == "WLED-AP"
    assert cfg_object["ap"]["pskl"] == 8
    assert cfg_object["ap"]["ip"] == [4, 3, 2, 1]
    print("OK!")

    print("\tValidating no modem sleep enabled... ", end="")
    assert cfg_object["wifi"]["sleep"] is False
    print("OK!")

    print("\tValidating Network SSID is set... ", end="")
    assert type(cfg_object["nw"]["ins"][0]["ssid"]) == str
    print("OK!")
