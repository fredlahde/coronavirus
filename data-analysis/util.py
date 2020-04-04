import sys
def sort_dict(d, len = -1):
    ret = {}
    idx = 0
    for k in sorted(d, key=d.get, reverse=False):
        ret[k] = d[k]
        idx = idx +1
        if idx == len and len != -1:
            break
    return ret

def add_time_series(old, new):
    ret = {}
    for date, old in old.items():
        ret[date] = old + new[date]
    return ret

def run_action_on_arg(wanted, fn):
    for arg in sys.argv[1:]:
        if arg == wanted:
            fn()
