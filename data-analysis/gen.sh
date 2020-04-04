#!/bin/bash
countries=(Germany US Italy Spain China Austria Sweden)
set -e
set -x
mkdir -p png-rendered
cd COVID-19 && git pull origin master && cd ../

for c in ${countries[@]}; do
    python3 analyze.py "$c" --log --png --grid
done
mv *.png png-rendered
