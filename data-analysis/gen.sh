#!/bin/bash
set -e
set -x
curl -LO https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
curl -LO https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
curl -LO https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv

countries=(Germany US Italy Spain China Austria Sweden Australia)
mkdir -p png-rendered

for c in ${countries[@]}; do
    python3 analyze.py . "$c" --log --png --grid
done
python3 analyze.py . "Korea, South" --log --png --grid
mv *.png png-rendered

rm time_series_covid19_confirmed_global.csv
rm time_series_covid19_deaths_global.csv
rm time_series_covid19_recovered_global.csv
