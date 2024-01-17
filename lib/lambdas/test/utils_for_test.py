import json


def deep_sort(obj):
    """
    Recursively sort list or dict nested lists.
    """

    if isinstance(obj, dict):
        # Sort the dictionary by key, then sort the values recursively
        return {k: deep_sort(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
        # Attempt to sort the list. If this fails (e.g., if it contains dictionaries),
        # sort each item in the list recursively and turn them into tuples if they are dictionaries
        try:
            return sorted(deep_sort(x) for x in obj)
        except TypeError:
            # The list contains non-orderable items (like dictionaries), sort them as tuples
            return sorted(
                (k, deep_sort(v)) if isinstance(v, dict) else deep_sort(v)
                for k, v in (x.items() for x in obj)
            )
    else:
        # If obj is not a list or dict, return it as is
        return obj


def are_json_structures_equal(json1: dict, json2: dict):
    """
    Check if the given JSON structures are equal, after sorting them recursively.
    """
    sorted_json1 = deep_sort(json1)
    sorted_json2 = deep_sort(json2)

    with open("expected.json", "w") as f:
        json.dump(sorted_json1, f)
    with open("actual.json", "w") as f:
        json.dump(sorted_json2, f)

    return sorted_json1 == sorted_json2
