# WLED Config Toolkit
A Python/Command-line tool for modular configuration of WLED instances over the network.

## Features
* **Easy wireless configuration**: Set up multiple WLED instances without the hassle of manual configuration.
* **Reproducible**: Easily replicate WLED configurations for friends, events, or new installations.
* **Maintainable**: Use modular JSON configs to share and override settings across multiple instances.
* **Friendly naming**: Optional hostname/mDNS support lets you use names instead of IP addresses for your WLEDs.
* **Offline operation**: No internet connection required to upload configuration.
* **Validation**: Optional verification of config after uploading ensures successful updates.

## Getting Started
1. Install Python (3.10+) if you don't have it.

2. Open a terminal in this directory and run `pip install -r requirements.txt` to install the required packages.
3. [Get your cfg.json files][getting_cfgs] from your running WLED instances and save them in the `/data/cfg_modules/` directory with descriptive names.
4. Create your `wled-config.json` file by duplicating `data/example_simple_conf.json` to `my_conf.json`.\
   Update the IP addresses, names, and `cfg_modules` to match your WLED instances.
5. (Optional) [Create some overrides](./docs/Creating_Override_Cfg_Modules.md) and update your wled-config file to use them.
6. Run the CLI with the command `python wled_config_cli my_conf.json --build --upload --verify-upload`.

For more detailed information and advanced usage, see the [Advanced Usage][advanced_usage] documentation.

> ⚠️ **Warning**: Uploading replaces your entire cfg.json file. Any missing properties will be reset to WLED's defaults.
>
> For this reason, it's recommended to always have some `base_cfg.json` that's initially ripped from your WLED, and only removing what you plan to override.
> This tool has some validation to check critical things like AP config hasn't changed, and WIFI has an SSID, but there can still be data loss.

## Integrating into python projects
To use the python API, take a look at [src/example_run_config_build.py](src/example_run_config_build.py) as an example.

## How does it work
WLED configuration can be mostly handled with [cfg.json](https://kno.wled.ge/interfaces/json-api/) files. <br/>
The config CLI lets you create a bunch of of these "cfg_modules" and provides a layer above these files called `wled-config.json`.

For more information about the structure and keys of the cfg.json file, check out [cfg_json_structure.md](./docs/Cfg_Json_Structure.md).


### wled-config.json files
These are files containing the actual WLED instances (as IP addresses or mDNS names)
each instance can define what cfg.json modules it will use


### cfg_modules
These are cfg.json files, or parts of them, that are saved in the `cfg_modules` directory and can be reused between controllers/wled-config files.


## FAQ
TODO if common problems come up.

Feel free to [Open an issue](https://github.com/JonLevin25/Wled-Config-Toolkit/issues) if you encounter a problem or have a feature request.

[advanced_usage]: docs/Advanced_Usage.md
[getting_cfgs]: docs/Getting_Cfg_Json_From_A_WLED.md
