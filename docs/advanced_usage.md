# Advanced Usage
WLED configuration can be mostly handled with [cfg.json](https://kno.wled.ge/interfaces/json-api/) files. <br/>
The config CLI provides a layer above these files called `wled-config.json` files.

`wled-config.jsons` can define that a certain WLED (i.e. your living roon WLED) will receive a certain `cfg.json` (i.e. `livingroom_cfg.json`),

And your bedroom could receive another (`bedroom_cfg.json`).

For more advanced usage, you could have smaller building blocks and _compose_ a WLED instance out of these.
These building blocks could be files like `base_cfg.json`, `8am_timer_cfg.json`, `cfg_digital_mic_pins.json`,
`freds_wifi.json`, etc.

### cfg.json keys
As noted above, the `.wled-config.json` may use cfg_modules or direct json, but in the end they are all built into a **single WLED cfg.json per instance.** <br/>
To learn about these, you can check out the [WLED json api page](https://kno.wled.ge/interfaces/json-api/).
Most of the keys there are relevant to cfg.json.

## Wled-config file structure
each key in a `wled-config` file is an identifier of a WLED instance - either an IP or [MDNS](#what-is-mdns-anyway)

This is the main config object used -
you can define wled json keys in 2 ways:
* Loading config from files via the `cfg_modules` property
* Specifying JSON directly via the `overrides` property
There's a fairly comprehensive guid to defining config in the [data folder](./data/README.md)

### cfg_modules
these are JSON files contained in the `cfg_modules` subdirectory that can be reused between controllers/wled-config files.\
Specifying the `.json` extension for them is optional.

For example, this wled-config file defines two WLED instances: `wled-livingroom` and `wled-bedroom`.
Each one has their own `cfg.json` cfg_module that will be uploaded
```json
{
  "wled-livingroom": {
    "cfg_modules": ["cfg_livingroom.json"]
  },
  "wled-bedroom": {
    "cfg_modules": ["cfg_bedroom.json"]
  }
}
```
`cfg_modules` is an array.
You can add multiple *cfg.json* cfg_modules to have smaller, more reusable building blocks!
i.e.
```json
{
  "wled-livingroom": {
    "cfg_modules": ["cfg_shared", "cfg_livingroom","cfg_timer_6am", "cfg_button_set_twinkle"]
  },
  
  "wled-bedroom": {
    "cfg_modules": ["cfg_shared", "cfg_bedroom", "cfg_timer_6am"]
  }
}
```
Notice I've lost the`.json` suffix - it's optional.
In this case each WLED instance uses a few cfg.json cfg_modules - "cfg_shared", "cfg_livingroom", etc..
If the same keys are defined in both, later cfg_module will override the previous. 

### $common
In the example above we have some shared cfg_modules: `cfg_shared` and `cfg_timer_6am`.
To be clearer and less verbose, we set config-global configs in a `$common` object.
This wled-config file will be identical to the last one,
as wled-livingroom & wled-bedroom will implicitly prepend the shared cfg_modules.


```json
{
  "$common": {
    "cfg_modules": ["cfg_shared", "cfg_timer_6am"]
  },
  "wled-livingroom": {
    "cfg_modules": ["cfg_livingroom", "cfg_button_set_twinkle"]
  },
  
  "wled-bedroom": {
    "cfg_modules": ["cfg_bedroom"]
  }
}
```

### Overrides
If you'd rather define the json directly rather than in a cfg_module,
you can use the `overrides` property, like so
```json
{
  "wled-livingroom": {
    "cfg_modules": ["cfg_livingroom"],
    "overrides": {"if": {"live": {"dmx": {"uni": 7}}}}
  }
}
```
This wled-config file has one WLED instance called `wled-livingroom`, which has a config cfg_module called `cfg_livingroom`.
But it also has a direct JSON override to set the DMX to universe 7.

Override objects are the same as cfg_modules, except they're not in a separate json file, rather the wled-config itself.

###What is MDNS Anyway?
mDNS stands for MulticastDNS (Domain name system).
It's a way of giving a device a human-readable name on your local network.
Normally, you access your WLED device with an ip, by entering something like `192.168.1.4` into your browser.
With mDNS, you could just enter `http://wled-livingroom.local`!

this can be extremely convenient for:
* quickly opening a browser on an instance
* identifying different instances at a glance
* maintaining configuration for multiple instances

On windows, installing Bonjour print services is necessary for it to work. 
<div style="background-color: #ff666688">
WARNING: mDNS can be very finnicky (it may suddenly stop working until playing with the network).<br/>
Thus, while super convenient in development/tinkering, it's not recommended for production/exhibits/etc.
In these cases, either use static IPs or an IP to mDNS scanner can bridge the gap.
Feel free to open an issue if you'd like such a scanner as part of this tool.
</div>

Mainly, it lets you enter `http://my-wled.local` in your browser insta