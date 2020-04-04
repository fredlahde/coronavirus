#!/bin/bash
countries=(Germany US Italy Spain China Austria Sweden)
mkdir -p png-rendered
#cd COVID-19 && git pull origin master && cd ../

ls
pwd
for c in ${countries[@]}; do
    python3 analyze.py "$c" --log --png --grid
done
mv *.png png-rendered
