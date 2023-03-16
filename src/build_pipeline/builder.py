import time
from typing import Iterable

from src.config_build import *
from src.config_build.build_helpers import get_mdns_names_from_conf, get_cfg_file_path

from .CONFIG_ACTION import *


def run_build(settings: BuildSettings, actions: Iterable[CONFIG_ACTION]):
    conf_partial_build = settings.cfgs_to_build
    renames: Dict[str, str] = settings.renames or dict()

    if renames:
        if conf_partial_build:
            renames = {oldName: newName for oldName, newName in renames.items() if
                       newName in conf_partial_build or oldName in conf_partial_build}
        print(f'USING RENAMES_MAP ("old": "new") - {renames}')

    if CONFIG_ACTION.BUILD_AND_WRITE in actions:
        mdns_to_cfg_map = build_cfg_jsons_from_conf(settings)
        mdns_file_map_no_renames = write_cfg_jsons(mdns_to_cfg_map, settings)
        mdns_names = list(mdns_file_map_no_renames.keys())
    else:  # if not building, get list of existing generated files
        mdns_names = get_mdns_names_from_conf(settings.conf_file_path, conf_partial_build)
    mdns_names.extend(list(renames))
    mdns_to_files_map = {mdns: get_cfg_file_path(mdns, settings.cfg_cache_dir, renames_old_to_new=renames) for mdns in
                         mdns_names}

    if CONFIG_ACTION.UPLOAD in actions:
        failed_uploads = upload_cfg_files(mdns_to_files_map, reboot_after_upload=True)  # reboot doesnt work so well
        print(f'Finished uploading! File: {settings.conf_file_path}. Overrides: {conf_partial_build}')
        if failed_uploads:
            print(f'\nFAILED UPLOADS: {json.dumps(failed_uploads, indent=2)}')

    elif CONFIG_ACTION.UPLOAD_WLED_AP_4321 in actions:
        if renames:
            # renames might be trivial (just need figure out if you have 1 or two panels)
            raise ValueError("Uploading to 4.3.2.1 does not currently support renames!")
        if len(mdns_names) != 1:
            raise ValueError(f"Expect only ONE override panel when uploading to WLED AP (4.3.2.1). "
                             f"Actual: {len(conf_partial_build)}")
        panel = mdns_names[0]
        cfg_json = mdns_to_files_map[panel]
        upload_to_wled_ap(cfg_json, panel)
        print("Sleeping for 3sec in case configs changed")
        time.sleep(3)

    if CONFIG_ACTION.TEST_COMPARE_ACTUAL_CONFIGS_TO_EXPECTED in actions:
        verify_test_live_panels(mdns_to_files_map)

    if renames:
        print(f'\n (RENAMES IN USE - Might see some errors from name changes, or trying both new and old MDNS\'s')
