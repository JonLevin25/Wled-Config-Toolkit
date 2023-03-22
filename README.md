# WLED Config Toolkit

A Python/Command-line tool for modular configuration of WLED instances over the network.

## Features

- **Easy wireless configuration**: Set up multiple WLED instances without the hassle of manual configuration.
- **Reproducible**: Easily replicate WLED configurations for friends, events, or new installations.
- **Maintainable**: Use modular JSON configs to share and override settings across multiple instances.
- **Friendly naming**: Optional hostname/mDNS support lets you use names instead of IP addresses for your WLEDs.
- **Offline operation**: No internet connection required to upload configuration.
- **Validation**: Optional verification of config after uploading ensures successful updates.

For a list of what you can actually configure with `cfg.json`, [See here](./docs/Cfg_Json_Structure.md)

## Getting Started

1. Clone or download this repository
2. Install Python (3.10+) if you don't have it.
3. Make sure Python is in the system PATH (open a terminal in this folder and enter `python --version`)
4. Install `requirements.txt`. Easiest way: in a terminal enter `python -m pip install -r requirements.txt`. This will install the packages globally.
5. [Get your cfg.json files][getting_cfgs] from a running WLED instances and save them in `/data/cfg_modules/`
6. Create your `wled-conf.json` file by duplicating `data/example_simple_conf.json` and renaming it `simple.wled-conf.json`.
7. Open the `simple.wled-conf.json` you created, change the IP address and names
8. If you used a name other than `cfg_base.json` for your cfg template, make sure you use the same name in the `wled-conf` file.
9. Run the CLI with the command `python wled-config-toolkit.py data/simple.wled-conf.json --build --upload --verify-upload`.
10. you should see something like this:

```cmd
Loading wled-conf file: data/simple.wled-conf.json
Building wled-conf file: data/simple.wled-conf.json
Generating config file for: 192.168.1.100
...
Testing live panels...
Testing 192.168.50.56:
         GET http://192.168.50.56/json/cfg.json... 200
         Compare JSON to expected: match OK
        Setting test colors (default, r, g, b)...OK
HTTP Verification Finished
Verification OK!
```

## Customizing config

After you have a working `wled-conf` file, you can customize it by adding more instances, [adding overrides](./docs/Creating_Override_Cfg_Modules.md) per instance, or creating multiple `wled-conf` files for different usages.

For more detailed information and advanced usage, see the [Advanced Usage][advanced_usage] documentation.

> ⚠️ **Warning**: Uploading replaces your entire cfg.json file. Any missing properties will be reset to WLED's defaults.
>
> For this reason, it's recommended to always have some `cfg_base.json` that's initially ripped from your WLED, and only removing what you plan to override.
> This tool has some validation to check critical things like AP config hasn't changed, and WIFI has an SSID, but there can still be data loss.

## Integrating into python projects

To use the python API, take a look at [src/example_run_config_build.py](src/example_run_config_build.py) as an example.

## How does it work

WLED configuration can be mostly handled with [cfg.json](https://kno.wled.ge/interfaces/json-api/) files. <br/>
The config CLI lets you create a bunch of of these "cfg_modules" and provides a layer above these files called `wled-conf.json`.

For more information about the structure and keys of the cfg.json file, check out [cfg_json_structure.md](./docs/Cfg_Json_Structure.md).

### wled-conf.json files

These are files containing the actual WLED instances (as IP addresses or mDNS names)
each instance can define what cfg.json modules it will use

### cfg_modules

These are cfg.json files, or parts of them, that are saved in the `cfg_modules` directory and can be reused between controllers/wled-conf files.

## FAQ

TODO if common problems come up.

Feel free to [Open an issue](https://github.com/JonLevin25/wled-conf-Toolkit/issues) if you encounter a problem or have a feature request.

[advanced_usage]: docs/Advanced_Usage.md
[getting_cfgs]: docs/Getting_Cfg_Json_From_A_WLED.md
