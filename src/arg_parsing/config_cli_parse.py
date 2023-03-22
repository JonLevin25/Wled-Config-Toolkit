import argparse

from src.build_pipeline import CONFIG_ACTION
from src.settings import BuildSettings
from src.settings.consts import *


class ConfigCLIArgs(argparse.Namespace):
    config: str
    build: bool
    build_cached: bool
    upload: bool
    upload_ap: bool
    verify_upload: bool
    cfg_modules_dir: str
    cache_dir: str


def parse_config_args() -> ConfigCLIArgs:
    parser = argparse.ArgumentParser(description='WLED Config Toolkit')

    # Main param - wled-conf file
    parser.add_argument('config', metavar='wled-conf.json', help='path to wled-conf.json file')

    # Build Actions - build&write, upload, verify
    build_group = parser.add_mutually_exclusive_group(required=True)
    build_group.add_argument('-b', '--build', action='store_true', help='build all cfg.jsons from the  wled-conf file given')
    build_group.add_argument('--build-cached', action='store_true',
                             help='Use the wled-conf file only for the names of instances, but use already built configs from the output dir')

    upload_group = parser.add_mutually_exclusive_group()
    upload_group.add_argument('-u', '--upload', action='store_true',
                              help='upload cfg.jsons to the ip/mdns given (wled-conf file keys). Requires being on the same network and the instances being on and discoverable.')
    upload_group.add_argument('--upload-ap', action='store_true',
                              help='upload cfg.jsons to WLED-AP (4.3.2.1). Requires being connected to the AP directly.')

    parser.add_argument('--verify-upload', action='store_true',
                        help='attempt to verify the success of uploads by checking the instance state.')

    # settings - module/output dirs, etc
    parser.add_argument('--cfg-modules-dir', help='path to cfg.json modules directory', default=DEFAULT_CFG_MODULES_DIR)
    parser.add_argument('--cache-dir', help='path to where cfg.jsons will be output before uploading',
                        default=DEFAULT_CACHE_DIR)

    # todo: partial build (arg list)
    # todo: renames (separate command??)

    # Help examples
    parser.usage = parser.format_usage() + f"""Examples:
    
    python wled-config-toolkit.py --build --upload --verify-upload <your.wled-conf.json>
    python wled-config-toolkit.py -bu --verify-upload <your.wled-conf.json>
    python wled-config-toolkit.py -bu --verify-upload --cfg-modules-dir="data/cfg_modules" --cache-dir="data/generated" <your.wled-conf.json>
    """

    return parser.parse_args(namespace=ConfigCLIArgs())


def args_to_settings(args: ConfigCLIArgs) -> (BuildSettings, set[CONFIG_ACTION]):
    settings = BuildSettings(args.config, args.cfg_modules_dir, args.cache_dir,
                             cfgs_to_build=None,
                             renames=None)

    def add(arg, config: CONFIG_ACTION):
        return config if arg else None

    actions = \
        {
            add(args.upload, CONFIG_ACTION.UPLOAD),
            add(args.build, CONFIG_ACTION.BUILD_AND_WRITE),
            add(args.upload_ap, CONFIG_ACTION.UPLOAD_WLED_AP_4321),
            add(args.verify_upload, CONFIG_ACTION.TEST_COMPARE_ACTUAL_CONFIGS_TO_EXPECTED),
        } - {None}

    return settings, actions
