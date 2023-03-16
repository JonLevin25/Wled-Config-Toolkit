from typing import Union, Iterable, Dict

from src.settings.consts import *


class BuildSettings:
    def __init__(self,
                 conf_file_path: str,
                 cfg_modules_dir: str = DEFAULT_CFG_MODULES_DIR,
                 cfg_cache_dir: str = DEFAULT_CACHE_DIR,

                 # use if you want to select only some of the cfgs in a wled-config file to build
                 cfgs_to_build: Union[str, Iterable[str]] = None,
                 renames: Dict[str, str] = None  # format- {oldName: newName}
                 ):
        self.conf_file_path = conf_file_path
        self.cfg_modules_dir = cfg_modules_dir
        self.cfg_cache_dir = cfg_cache_dir
        self.cfgs_to_build = cfgs_to_build
        self.renames = renames
