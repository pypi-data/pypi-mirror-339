#!/bin/bash

rm -fr tmp

echo -e "\nCreating Dirs\n"

mkdir -p tmp/node_modules
mkdir -p tmp/tmp/node_modules
mkdir -p tmp/tmp/tmp/node_modules

find . -name node_modules -type d

echo -e "\nRun: python -m remove.main **/node_modules\n"

shopt -s globstar
python -m remove.main **/node_modules
