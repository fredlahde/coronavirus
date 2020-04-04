#!/bin/bash
set -e
set -x
countries=(Germany US Italy Spain China Austria Sweden Australia)
mkdir -p png-rendered

for c in ${countries[@]}; do
    python3 analyze.py "$c" --log --png --grid
done
python3 analyze.py "Korea, South" --log --png --grid
mv *.png png-rendered
