# Creating Override Configs

If you have multiple WLED instances, you might find it useful to break the configuration into multiple files. This allows you to create a base configuration and add overrides for instance-specific properties.

**NOTE**: Before using overrides, you'll want to also [get your wled's cfg.json file][get_cfg_json] and create a `cfg_base.json`

See [WLED cfg.json structure](./Cfg_Json_Structure.md) for more info on what config keys are available and what they mean.

## Example

Lets create a couple overrides for the number of led strips for different WLED instances.

### Creating cfg_modules

To do this, lets create a coule `cfg_modules`.

- `cfg_strips_1x100.json` will define 1 strips of 100 leds, on pin , on pins 13
- `cfg_strips_2x100.json` is similar, but it defines 2 strips, on pins 13 and 14

To get started, were going to use these example files:

- `./data/cfg_modules/example_strips_1x100.json`
- `./data/cfg_modules/example_strips_2x100.json`
- `./data/example_home.wled-conf.json`

To follow along, you can rename them by removing the `example_` prefix.

<details open>
<summary><b>/data/cfg_modules/cfg_strips_1x100.json</b></summary>

```json
{
  "hw": {
    "led": {
      "ins": [
        {
          "start": 0,
          "len": 100,
          "pin": [13],
          "order": 0,
          "rev": false,
          "skip": 0,
          "type": 22,
          "ref": false
        }
      ]
    }
  }
}
```

</details>
<details>
<summary><b>/data/cfg_modules/cfg_strips_2x100.json</b></summary>

```json
{
  "hw": {
    "led": {
      "ins": [
        {
          "start": 0,
          "len": 100,
          "pin": [13],
          "order": 0,
          "rev": false,
          "skip": 0,
          "type": 22,
          "ref": false
        },
        {
          "start": 100,
          "len": 200,
          "pin": [14],
          "order": 0,
          "rev": false,
          "skip": 0,
          "type": 22,
          "ref": false
        }
      ]
    }
  }
}
```

</details>

The config is nested- hw (hardware) -> "led" -> "ins". Instances is the array of our led configs.

While not strictly necessary for this tutorial, here are what the keys from the config mean if you're curious:

<details>
<summary>Led config keys</summary>

| Key   | Description                       | Notes                                                                               |
| ----- | --------------------------------- | ----------------------------------------------------------------------------------- |
| start | what index the led starts at      | Should generally be 0 for the first strip, or the index the last strip ended at     |
| len   | The strip length (number of leds) |                                                                                     |
| pin   | the pins the strip will use       | For 3-pin strips, this should always be a single pin enclosed in square brackets [] |
| order | Led color order                   | 0 is GRB (Default)                                                                  |
| rev   | Should the strip be reversed?     |                                                                                     |
| Skip  | Should skip the 1st led?          |                                                                                     |
| type  | The type of led strip             | 22 is WS281x                                                                        |

</details>

## Setting up the wled-conf.json

Now that you have 2 config modules (`cfg_strips_1x100.json`, `cfg_strips_2x100.json`)

You can use them in your wled-conf.json file, to **_override_** your `cfg_base.json`

<details open>
<summary><b>/data/home.wled-conf.json</b></summary>

```json
{
  "$common": { "cfg_modules": ["cfg_base"] },
  "wled-bedroom": {
    "cfg_modules": ["cfg_strips_2x100"]
  },
  "wled-livingroom": {
    "cfg_modules": ["cfg_strips_1x100"]
  }
}
```

</details>

Make sure to replace `wled-livingroom`/`wled-bedroom` with your WLEDs mDNS or IP.

**Note:** The `home.wled-conf` example uses mDNS for the keys, which will automatically set mdns/name properties.
This requires zeroconf/mDNS to be available, and the mDNS to already be set.

To simply use IPs, see the `simple.wled-conf.json` example, replace `wled-bedroom`/ etc with your WLED IP, and optionally add the `name` override to find it easier in the app/web UI.

This approach allows you to maintain identical configurations while defining differences between them as overrides. You can override almost any setting available in the WLED web GUI (buttons, timers, pins, LED counts, Wi-Fi settings, etc.).

To upload this config run `python wled-config-toolkit.py -bu --verify-upload data/home.wled-conf.json`\

Note: Depending on your use case, you may or may not want to have a default setting for leds in your `cfg_base.json`.
Check the examples in the [cfg_modules directory][cfg_modules] for more ideas on how to compose different configs.

[get_cfg_json]: ./Getting_Cfg_Json_From_A_WLED.md
