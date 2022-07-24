#!/bin/bash

rm -f source.zip
git archive -o source.zip HEAD server

TEMP=$(mktemp -d)

cd $TEMP
mkdir -p ./server/app
echo flag{this_is_not_the_real_flag} > ./server/app/flag.txt
zip $OLDPWD/source.zip ./server/app/flag.txt

rm -rf $TEMP
