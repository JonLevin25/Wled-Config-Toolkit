# Tool extraction TODOs

## TODOS

### General

- rename `wled-config-cli.py` -> `wled-config-toolkit.py`

### Main Readme.md

- add 'clone or download git reepo'
- Python - when installing make sure to Add python to system PATH
- suggested conf name - `myconf.wled-conf.json`
- change name in example command as well

command (script name, extension + conf example name): `python wled-config-cli.py data/myconf.wled-conf.json --build --upload --verify-upload`

- package (global) install command `python -m pip install -r requirements.txt`.

  - note that virtualenv is recommmended, but less straight-forward

- split Update IP addresses/etc to own numbered bullet
- wifi guard
- align naming: `.wled-conf.json` or `wled-config.json`

### Getting WLED cfg

- break apart intro to intro + `Why start with the WLED cfg.json`? section
- move NOTE into `get cfg` section
- if WLED connected to your home network
  - How to get your WLED IP (discovery from app, add WLED link for this)
- if from WLED-AP: connect to it's wifi and config WIFI.
  - Note there's a more advanced way to do it when you're on the WLED-AP itself, using the no-network method + the --upload-ap
  - click on cfg.json ...the text in the right pane (which should look something like `{"rev": [...`) is your `cfg.json`
  - next section: you need to save the json as a new file in the `./data/cfg_modules/` directory. \
    Suggested name is `base_cfg.json`, since this is the base file you will be overriding.
  - cfg_modules_directory link - make path clearer ()

## General plan

---

### Repo + flow test

6. Test FOSS repo flow
   - In VM: install Python 3.10
   - follow readme instructions
   - create conf file from example
   - test build+upload+verify wled-config file

---

## v2 (NOT NOW)

- add tests
- Partial build support
- Renaming support (add json file, dont deal with cmdline args)
- JSON with comments / JSON5 support for wled-config/cfg files? (build into JSONs)
- add "ip" property to wled-config files, so you can define them inside the objects
- Automate fetching config into /data/fetched? (to get running configs for later override)

## v3

- Port to node.js?
- Nice GUI?
