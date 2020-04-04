import os
import matplotlib.pyplot as plt
import math
import sys
PATH = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series"

LOG = False

class TimeSeriesReportEntry():
    def __init__(self, country, confirmed_series, death_series, recovered_series):
        self.country = country
        self.confirmed_series = confirmed_series
        self.death_series = death_series
        self.recovered_series = recovered_series

def parse_first_line(line):
    split = line.split(',')
    dates = []
    for i in range(4, len(split)):
        dates.append(split[i])
    return dates

def parse_line(line, dates):
    """
    format:
    0: state
    1: country
    2: lat
    3: lng
    4 and further: time series
    """
    split = line.split(',')
    if len(split) < 2:
        return None
    country = split[1]
    time_series = {}
    date_idx = 0
    global LOG
    for i in range(4, len(split)):
        val = float(split[i])
        if val > 0:
            try:
                if LOG:
                    val = math.log2(val)
            except ValueError:
                print(val)
                exit(234)
        time_series[dates[date_idx]] = val
        date_idx = date_idx + 1
        if date_idx > len(dates) -1:
            break
    return country, time_series

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

def parse_file(f):
    lines = {}
    with open(f, 'r') as fd:
        text = fd.read()
        split = text.split('\n')
        dates = parse_first_line(split[0])
        for s in split[1:]:
            parsed =  parse_line(s, dates)
            if parsed is None:
                continue
            country, ts = parsed
            if country in lines:
                lines[country] = add_time_series(lines[country], ts)
            else:
                lines[country] = ts
    return lines


def parse_all():
    ret = {}
    confirmed_file = os.path.join(PATH, "time_series_covid19_confirmed_global.csv")
    deaths_file = os.path.join(PATH, "time_series_covid19_deaths_global.csv")
    recovered_file = os.path.join(PATH, "time_series_covid19_recovered_global.csv")
    confirmed = parse_file(confirmed_file)
    deaths = parse_file(deaths_file)
    recovered = parse_file(recovered_file)

    for country, c in confirmed.items():
        d = deaths[country]
        r = recovered[country]
        ret[country] = TimeSeriesReportEntry(country, c,d,r)

    return ret

def print_dicht(m, style, label):
    m = sort_dict(m)
    vals = list(m.values())
    keys = list(m.keys())
    plt.plot_date(keys, vals,style)

def analyze(country):
    parsed = parse_all()

    country_data = parsed[country]

    print_dicht(country_data.confirmed_series, 'b', "confirmed")
    print_dicht(country_data.death_series, 'r', "deaths")
    print_dicht(country_data.recovered_series, 'g', "recovered")
    plt.xticks(rotation=90)
    plt.show()
    #parsed = [p for p in parse_file(f) if p is not None]
    #foo(parsed)

def print_usage():
    print("Usage: %s <country> [--log]" % sys.argv[0])
    exit(1)

if len(sys.argv) == 1:
    print_usage()

for arg in sys.argv[1:]:
    if arg == "--help":
        print_usage()

country = sys.argv[1]
if len(sys.argv) > 2 and sys.argv[2] == "--log":
    LOG = True
analyze(country)
