from typing import List

from src.utils.json_utils import resolve_json_to_object, json_str_file_or_object


def _override_values(override_vals: List):
    override_vals = [j for j in override_vals if j is not None]  # filter None's for now.

    if len(override_vals) == 0:
        return None

    val_type = type(override_vals[0])
    assert (all((type(t) == val_type for t in override_vals)))

    if val_type == dict:
        return _override_keys_dict(override_vals)
    elif val_type == list:
        return _override_keys_array(override_vals)

    # use last override if multiple
    else:
        return override_vals[-1]


def _override_keys_dict(json_objects: List):
    assert (all((type(ovr) == dict for ovr in json_objects)))  # Only dics (and no None's!) allowed at this point
    assert (all(ovr is not None for ovr in json_objects))

    all_keys = set((key for j in json_objects for key in j.keys()))

    def get_value(key):
        sources = (j for j in json_objects if key in j)
        return _override_values([source[key] for source in sources])

    return {key: get_value(key) for key in all_keys}


def _override_keys_array(all_jsons: List[List]):
    assert (all((type(j) == list for j in all_jsons)))  # Only dics (and no None's!) allowed at this point

    max_len = max((len(x) for x in all_jsons))

    def get_value(i):
        sources = (j for j in all_jsons if len(j) > i)
        return _override_values([source[i] for source in sources])

    return [get_value(i) for i in range(max_len)]


def generate_json_with_overrides(*overrides: json_str_file_or_object):
    override_jsons = [resolve_json_to_object(ovr) for ovr in overrides]
    return _override_values(override_jsons)
