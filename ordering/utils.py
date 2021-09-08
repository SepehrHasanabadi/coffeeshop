# remove all specific keys from dictionary or list items
def remove_keys(d, keys):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_keys(v, keys) for v in d]
    return {k: remove_keys(v, keys) for k, v in d.items()
            if k not in keys}

# sort whole items of a list or a dictionary
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj