def stringify_dict(d: dict):
    return ", ".join("-".join((str(k), str(v))) for k, v in d.items())
