#!/bin/sh

set -x
set -e
set -o pipefail

./satellite-sanity -h | grep --quiet 'Check Red Hat Satellite sanity'
./satellite-sanity --list-tags | grep --quiet '^Satellite_5$'
./satellite-sanity --list-tags | grep --quiet '^general$'
./satellite-sanity --list-rules | grep --quiet '^Selected tag(s): general$'
./satellite-sanity --list-rules | grep --quiet '^Just a demo rule which keeps failing (example_fails); tags: general$'
./satellite-sanity --tags general --list-rules | grep --quiet '^Selected tag(s): general$'
./satellite-sanity --tags Satellite_5 --list-rules | grep --quiet '^Selected tag(s): Satellite_5$'
./satellite-sanity --tags general,Satellite_5 --list-rules | grep --quiet '^Selected tag(s): general, Satellite_5$'
./satellite-sanity --tags general --list-rules | wc -l | grep '^4$'
if ./satellite-sanity --tags general; then false; else true; fi
