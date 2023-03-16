import json
from os import path
from pathlib import Path
from typing import Dict, Any, List

from src.networking.web_utils import is_valid_ip
from src.settings import BuildSettings
from src.utils.json_override import generate_json_with_overrides
from src.utils.json_utils import resolve_json_filepath, resolve_json_to_object
from .build_helpers import get_cfg_json_value_name_mdns, get_cfg_file_path, extract_json_conf_data, \
    get_mdns_names_from_conf


def write_cfg_jsons(mdns_to_cfg_map: Dict[str, str], settings: BuildSettings, indent=2) -> Dict[str, str]:
    """
    write the given map of hostnames to cfg.json files.
    Returns a map from the same hostnames to files.
    """

    # all names: strictly loaded wled-config object
    all_names = [*mdns_to_cfg_map]
    mdns_to_filepath_map = {name: get_cfg_file_path(name, settings.cfg_cache_dir, settings.renames) for name in
                            all_names}
    for mdns_name in all_names:
        json_str = mdns_to_cfg_map[mdns_name]
        filepath = Path(mdns_to_filepath_map[mdns_name])
        dirpath = filepath.parent
        dirpath.mkdir(parents=True, exist_ok=True)
        with filepath.open('w+') as file:
            json.dump(json_str, file, indent=indent or None)
            print(f'generated cfg: {path.relpath(filepath, settings.cfg_cache_dir)}')
    return mdns_to_filepath_map


def build_cfg_jsons_from_conf(settings: BuildSettings) -> Dict[str, Any]:
    print(f"Loading wled-config file: {settings.conf_file_path}")
    loaded_conf = resolve_json_to_object(settings.conf_file_path)
    print(f"Building wled-config file: {settings.conf_file_path}"
          f"{f'(configs: {settings.cfgs_to_build})' if settings.cfgs_to_build else ''}")

    # Add all cfg.jsons to our map
    cfg_json_map = {}
    common_cfg_modules, common_overrides = extract_json_conf_data(loaded_conf, '$common', settings.cfg_modules_dir)

    # TODO: Test override_names
    names = get_mdns_names_from_conf(loaded_conf, settings.cfgs_to_build)
    if len(names) == 0:
        raise Exception("No configs to build! (Did you do a partial build with names that aren't in the wled-config file?)")
    for mdns_or_ip in names:
        print(f"Generating config file for: {mdns_or_ip}")

        built_cfg_json = build_cfg_json(
            loaded_conf, mdns_or_ip, common_cfg_modules, common_overrides, settings.cfg_modules_dir)

        cfg_json_map[mdns_or_ip] = built_cfg_json

    return cfg_json_map


def build_cfg_json(conf_obj: Dict[str, Any], mdns_or_ip: str, common_cfg_modules: List[str],
                   common_overrides: Dict[str, Any], cfg_modules_dir: str):
    print("\t...extracting cfg_modules/overrides")
    my_cfg_modules, my_overrides = extract_json_conf_data(conf_obj, mdns_or_ip, cfg_modules_dir)

    print("\t...adding $common cfg_modules/overrides")
    all_cfg_modules = [*common_cfg_modules, *my_cfg_modules]
    all_overrides = [common_overrides, my_overrides]

    # set "name" override only if not given an ip address
    if not is_valid_ip(mdns_or_ip):
        print("\t...Adding MDNS + Name")
        name_override = get_cfg_json_value_name_mdns(mdns_or_ip)
        all_overrides.append(name_override)

    missing_module_files = [t for t in all_cfg_modules if not resolve_json_filepath(t)]
    if missing_module_files:
        raise FileNotFoundError(f"Missing JSON module files: {missing_module_files}")

    print("\t...building final cfg.json")
    built_cfg_json = generate_json_with_overrides(*all_cfg_modules, *all_overrides)
    return built_cfg_json
