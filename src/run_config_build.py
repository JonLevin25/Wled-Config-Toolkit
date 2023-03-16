from src.build_pipeline import *
from src.settings import BuildSettings


def _custom_config_build():
    run_build(
        BuildSettings(
            conf_file_path=CONF_FILES.home,

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
    minis = "data/mini.wled-config.json"
    teder = "data/teder.wled-config.json"
    burn = "data/burn.wled-config.json"
    multi_panel_test = 'data/multi_panel_test.wled-config.json'
    science_museum = "data/science_museum.wled-config.json"
    home = "data/home.wled-config.json"


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
