from src.build_pipeline import *
from src.settings import BuildSettings

import os.path as path

CONFIG_DATA_DIR = "../wled-config-data"

def _custom_config_build():
    run_build(
        BuildSettings(
            conf_file_path=CONF_FILES.home,
            cfg_modules_dir=path.join(CONFIG_DATA_DIR, "cfg_modules"),
            cfg_cache_dir=path.join(CONFIG_DATA_DIR, "generated"),


            # To run the build for only some of the controllers in the wled-config file - define them here
            # cfgs_to_build=["192.168.50.3"],
            # To rename controllers:
            #    * first make sure CONF_FILE has the NEW names!
            #    * uncomment renames and format as below:
            #    * "oldName": newName"
            renames={"A": "shelves"}
        ),
        {
            # Note: You can't change the order of these operations
            # (i.e. writing to file will always happen before upload)
            # but you can enable or disable them by commenting (#) the line

            CONFIG_ACTION.BUILD_AND_WRITE,
            CONFIG_ACTION.UPLOAD,
            # CONFIG_ACTION.UPLOAD_WLED_AP_4321,
            CONFIG_ACTION.TEST_COMPARE_ACTUAL_CONFIGS_TO_EXPECTED,
        }
    )


class CONF_FILES:
    minis = path.join(CONFIG_DATA_DIR, "mini.wled-config.json")
    teder = path.join(CONFIG_DATA_DIR, "teder.wled-config.json")
    burn = path.join(CONFIG_DATA_DIR, "burn.wled-config.json")
    multi_panel_test = path.join(CONFIG_DATA_DIR, 'multi_panel_test.wled-config.json')
    science_museum = path.join(CONFIG_DATA_DIR, "science_museum.wled-config.json")
    home = path.join(CONFIG_DATA_DIR, "home.wled-config.json")


class CONTROLLERS_MDNS:
    """
    Controller MDNS/ips specified for easy access in build scripts.
    """
    mini_paciphea = "mini_paciphea"
    mini_minos = "mini_minos"
    mini_theseus = "mini_theseus"
    mini_pocidon = "mini_pocidon"


if __name__ == '__main__':
    _custom_config_build()
