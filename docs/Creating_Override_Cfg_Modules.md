# Creating Override Configs
If you have multiple WLED instances, you might find it useful to break the configuration into multiple files. This allows you to create a base configuration and add overrides for instance-specific properties.

**NOTE**: Before using overrides, you'll want to also [get your wled's cfg.json file][get_cfg_json] and create a `base_cfg.json`

See [WLED cfg.json structure](./Cfg_Json_Structure.md) for more info on what config keys are available and what they mean. 



## Example
Lets create a couple overrides for the number of led strips for different WLED instances.

### Creating cfg_modules
To do this, we'll create 2 cfg.json "cfg_modules":
- `cfg_strips_1x100.json` will define 1 strips of 100 leds, on pin , on pins 13
- `cfg_strips_2x100.json` is similar, but it defines 2 strips, on pins 13 and 14

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
          "pin": [
            13
          ],
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
          "pin": [
            13
          ],
          "order": 0,
          "rev": false,
          "skip": 0,
          "type": 22,
          "ref": false
        },
        {
          "start": 100,
          "len": 200,
          "pin": [
            14
          ],
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

The config is nested- hw (hardware) -> "led" -> "ins" (instances?).
Instances is the array of our led configs.

While not strictly necessary for this tutorial, here are what the keys from the config mean if you're curious:

<details>
<summary>Led config keys</summary>

| Key   | Description                       | Notes                                                                               |
|-------|-----------------------------------|-------------------------------------------------------------------------------------|
| start | what index the led starts at      | Should generally be 0 for the first strip, or the index the last strip ended at     |
| len   | The strip length (number of leds) |                                                                                     |
| pin   | the pins the strip will use       | For 3-pin strips, this should always be a single pin enclosed in square brackets [] |
| order | Led color order                   | 0 is GRB (Default)                                                                  |
| rev   | Should the strip be reversed?     |                                                                                     |
| Skip  | Should skip the 1st led?          |                                                                                     |
| type  | The type of led strip             | 22 is WS281x                                                                        |
</details>

## Setting up the wled-conf.json
In your wled-conf.json file, combine the base configuration and the overrides.

<details open>
<summary><b>/data/home.wled-conf.json</b></summary>

```json
{
  "$common": {"cfg_modules": [
    "cfg_base"
  ]},
  "wled-bedroom": {
    "cfg_modules": ["cfg_strips_2x100"]
  },
  "wled-livingroom": {
    "cfg_modules": ["cfg_strips_1x100"]
  }
}
```

</details>

This approach allows you to maintain identical configurations while defining differences between them as overrides. You can override almost any setting available in the WLED web GUI (buttons, timers, pins, LED counts, Wi-Fi settings, etc.).

Note: Depending on your use case, you may or may not want to have a default setting for leds in your `cfg_base.json`.

Check the examples in the [cfg_modules directory][cfg_modules] for more ideas on how to compose different configs.

[get_cfg_json]: ./Getting_Cfg_Json_From_A_WLED.md