#!/bin/bash

rm -fr tmp

echo -e "\nCreating Dirs\n"

mkdir -p tmp/node_modules
mkdir -p tmp/tmp/node_modules
mkdir -p tmp/tmp/tmp/node_modules

find . -name node_modules -type d

echo -e "\nRun: remove **/node_modules\n"

shopt -s globstar # feature available since bash 4.0, released in 2009
which remove
remove **/node_modules
