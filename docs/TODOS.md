# Tool extraction TODOs

## General plan

- Cleanup + extract my config data (leave examples)
- Turn into cli (take cmdline args)
- Extract to open source repo
- Make into submodule of `labyrinth_midburn`

Example:
`wled_cfg --config="home.conf.json"" -u --renames={"oldName": "newName"} --check-remote`

-----------------
### Repo + flow test
1. rename "templates" to "cfgs"
5. Setup FOSS repo
6. Test FOSS repo flow
   - In VM: install Python 3.10
   - follow readme instructions
   - create conf file from example
   - test build+upload+verify wled-config file
7. Labyrinth - use FOSS submodule

-------------------

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