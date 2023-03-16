import json
from json import JSONDecodeError
from typing import Union, Dict, List
from os import path

json_str_file_or_object = Union[str, dict]
json_value_types = Union[Dict, List, str, int, float]


def resolve_json_to_object(x: json_str_file_or_object):
    """
    Resolve either a:
        json string,
        json file path into a python object
        Or load an already made python Dict
    :param x:
    :return: the result of json.load or json.loads
    """
    if type(x) == dict:
        return x
    p = resolve_json_filepath(x)
    if p:
        with open(p, 'r') as file:
            try:
                return json.load(file)
            except JSONDecodeError as err:
                print(f"Error decoding JSON in File: {file}")
                raise file
    return json.loads(x)


def resolve_json_filepath(x: str):
    """
    Returns the path given if it exists, adding the .json extension if necessary.
    Returns None if the path does not exist
    """
    for p in [x, x + '.json']:
        if path.isfile(p):
            return p
    return None


def _compare_subset_json(subset: json_value_types, other: json_value_types) -> bool:
    if type(subset) != type(other):
        return False

    t = type(subset)
    if t == dict:
        if any(key not in other for key in subset):
            return False
        return all(_compare_subset_json(subset[key], other[key]) for key in subset)
    elif t == list:
        if len(subset) > len(other):
            return False
        return all(_compare_subset_json(subset[i], other[i]) for i in range(len(subset)))
    else:  # simple values
        return subset == other


def compare_subset_json(subset_json: json_str_file_or_object, other_json: json_str_file_or_object) -> bool:
    """
    Compares a small json string/file/object, to another object, that may have more properties than it
    :param subset_json: the json containing all the values you care to compare
    :param other_json: the other json. Properties not in subset_json, or additional array items, will be ignored.
    :return: True if all properties in subset_json exist and are the same in other_json. False otherwise
    """
    subset_obj = resolve_json_to_object(subset_json)
    other_obj = resolve_json_to_object(other_json)
    return _compare_subset_json(subset_obj, other_obj)
