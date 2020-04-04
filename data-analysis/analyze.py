import os
import matplotlib.pyplot as plt
import math
import sys
from util import *
from csv import *

PATH = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series"

LOG = False
PNG = False
GRID = False

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
    split = parse_csv_line(line)
    if len(split) < 2:
        return None
    country = split[1]
    time_series = {}
    date_idx = 0
    global LOG
    for i in range(4, len(split)):
        val = float(split[i])
        time_series[dates[date_idx]] = val
        date_idx = date_idx + 1
        if date_idx > len(dates) -1:
            break
    return country, time_series

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

def plot_dict(m, style, label):
    m = sort_dict(m)
    vals = list(m.values())
    keys = list(m.keys())
    plt.plot_date(keys, vals,style, label=label)

def build_title(country):
    global LOG
    virus = 'SARS-CoV-2'
    if LOG:
        fmt = virus + " in %s (logarithmically scaled)"
    else:
        fmt = virus + " in %s"
    return fmt % country

def analyze(country):
    global PNG
    global LOG
    global GRID
    parsed = parse_all()

    country_data = parsed[country]

    size = 10
    plt.figure(figsize=(size*3, size))
    plot_dict(country_data.confirmed_series, 'b', "confirmed")
    plot_dict(country_data.death_series, 'r', "deaths")
    plot_dict(country_data.recovered_series, 'g', "recovered")
    plt.xticks(rotation=90)
    plt.figlegend()
    if GRID:
        plt.grid(True, axis='x')
    if LOG:
        plt.yscale('log')
    plt.title(build_title(country))
    #plt.xscale(.5)
    if PNG == False:
        plt.show()
    else:
        plt.savefig('%s.png' % country.lower().replace(', ', '_'), orientation = 'landscape', dpi = 150)

def print_usage():
    print("Usage: %s <country> [--log]" % sys.argv[0])
    exit(1)

if len(sys.argv) == 1:
    print_usage()

run_action_on_arg("--help", print_usage)
def set_png():
    global PNG
    PNG = True
run_action_on_arg("--png" , set_png)

def set_grid():
    global GRID
    GRID = True
run_action_on_arg("--grid", set_grid)

def set_log():
    global LOG
    LOG = True
run_action_on_arg("--log" , set_log)

country = sys.argv[1]
analyze(country)
