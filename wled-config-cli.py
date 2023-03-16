#!/usr/bin/env python

from src.arg_parsing import parse_config_args, args_to_settings
from src.build_pipeline import run_build

if __name__ == '__main__':
    args = parse_config_args()
    settings, actions = args_to_settings(args)
    run_build(settings, actions)
    print(args.build)
    # pprint(args)
    # print(args.conf_file)
