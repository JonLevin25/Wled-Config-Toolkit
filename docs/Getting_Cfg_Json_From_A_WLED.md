# Getting cfg.json from a WLED instance
The cfg.json file is a configuration file that stores all the settings related to your WLED instance, such as LED strip configuration, Wi-Fi settings, timers, and more. It allows you to customize your WLED setup to match your specific needs and preferences.

## Why?
Instead of building a cfg.json from scratch, you can start with the current cfg.json from your WLED instance. This can help you get familiar with the structure of the configuration file and make it easier to customize it to your needs.

## Getting your WLEDs IP address
If you don't know your WLED's IP Address, you can open use discovery on the WLED mobile app (iOS AppStore/Google Play).

1. Make sure your phone is on the same network as the WLED (and your PC)
2. click the plus icon and hit "discover".
3. Wait a few seconds
4. Go back to the app main screen. If your WLED was discovered it should now show up with it's IP.
5. Write the IP down and use that in place of `<wled_ip>` in urls below.

If you could **not** discover your WLED IP, it may not be on your local network. look for a `WLED-AP` ssid and config the wifi.

## Get your cfg.json
**Notes**
* In the URLs below, replace `wled_ip` with your WLED's IP address or mDNS name.
* You always need to be on the same local network or Wi-Fi as your WLED.

**Option 1: Get cfg.json from WebUI (requires internet)**
1. Go to `http://<wled_ip>/edit`.
2. Click on `/cfg.json`
3. The `cfg.json` is the text in the right pane (that looks something like this: `{"rev": [...`)

**Option 2: Direct URL (works without internet)**
1. Go to `http://<wled_ip>/edit?edit=/cfg.json`.
2. This method returns the cfg.json directly without any UI.

## Save it to the modules directory
To use this JSON, you need to save the json as a new file in the [`./data/cfg_modules/`][cfg_modules] directory.\
The suggested name is `base_cfg.json`, since this is the base config you can override.

It's also a good idea to format the JSON file for easier reading and editing. Many text editors (like Visual Studio Code, Notepad++, etc.) have built-in formatting tools that support JSON.

If your editor doesn't have this feature, you can use an online tool to format the JSON, like [JSONLint](https://jsonlint.com).

[cfg_modules]: ../data/cfg_modules
