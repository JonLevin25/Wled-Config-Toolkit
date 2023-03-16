# Getting cfg.json from a WLED instance
The cfg.json file is a configuration file that stores all the settings related to your WLED instance, such as LED strip configuration, Wi-Fi settings, timers, and more. It allows you to customize your WLED setup to match your specific needs and preferences.
Instead of building a cfg.json from scratch, you can start with the current cfg.json from your WLED instance. This can help you get familiar with the structure of the configuration file and make it easier to customize it to your needs.

**Note**: In the URLs below, replace `wled_ip` with your WLED's IP address or mDNS name. You always need to be on the same local network or Wi-Fi as your WLED.

## Get your cfg.json
You can get the cfg.json file from your WLED instance using one of the following methods:

**Option 1: WebUI (requires an internet connection)**
1. Go to `http://<wled_ip>/edit`.
2. Click on `/cfg.json`.

**Option 2: Direct URL (works without an internet connection)**
1. Go to `http://<wled_ip>/edit?edit=/cfg.json`.
2. This method returns the cfg.json directly without any UI.

## Save it to the modules directory
To use this JSON, you need to give it a name and save it in the [cfg_modules directory][cfg_modules].

It's also a good idea to format the JSON file for easier reading and editing. Many text editors (like Visual Studio Code, Notepad++, etc.) have built-in formatting tools that support JSON.

If your editor doesn't have this feature, you can use an online tool to format the JSON, like [JSONLint](https://jsonlint.com).

[cfg_modules]: ../data/cfg_modules
