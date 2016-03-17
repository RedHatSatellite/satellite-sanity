#!/bin/sh

set -x
set -e
set -o pipefail

function bye() {
  echo "$1"
  exit ${2:-1}
}

./satellite-sanity -h | grep --quiet 'Check Red Hat Satellite sanity'
./satellite-sanity --list-tags | grep --quiet '^Satellite_5$'
./satellite-sanity --list-tags | grep --quiet '^general$'
./satellite-sanity --list-rules | grep --quiet '^Selected tag(s): general$'
./satellite-sanity --list-rules | grep --quiet '^Just a demo rule which keeps failing (example_fails); tags: general$'
./satellite-sanity --tags general --list-rules | grep --quiet '^Selected tag(s): general$'
./satellite-sanity --tags Satellite_5 --list-rules | grep --quiet '^Selected tag(s): Satellite_5$'
./satellite-sanity --tags general,Satellite_5 --list-rules | grep --quiet '^Selected tag(s): general, Satellite_5$'
./satellite-sanity --tags general --list-rules | wc -l | grep '^4$'

set +e
./satellite-sanity --tags general >/dev/null && bye "FAIL: Plain run failed" 1
./satellite-sanity --tags Satellite_5 >/dev/null && bye "FAIL: Plain run failed" 1   # check for this tag should fail
./satellite-sanity --tags general --rules example_fails >/dev/null && bye "FAIL: Run with specified rule failed" 1
./satellite-sanity --tags general --rules example_fails 2>&1 \
  | grep 'Selected rule(s): example_fails'
[ $? -eq 1 ] || bye "FAIL: Run with specified rule not prints whats expected" 1
./satellite-sanity --nagios-plugin --tags general >/dev/null
[ $? -eq 2 ] || bye "FAIL: Nagios exit code is not 2"
set +o pipefail
./satellite-sanity --nagios-plugin --tags general 2>&1 \
  | grep 'CRITICAL- Satellite sanity results: passed: 1, skipped: 1, failed: 1, unknown: 0 | Satellite sanity results: passed: 1, skipped: 1, failed: 1, unknown: 0'
[ $? -ne 0 ] && bye "FAIL: Nagios output is not correct" 1
./satellite-sanity --tags Satellite_5 2>&1 \
  | grep "ERROR: Some prerequisities were not met. Exiting. Maybe you want to add '--force'?"
[ $? -ne 0 ] && bye "FAIL: Failing check should mention '--force'" 1
./satellite-sanity --tags Satellite_5 --force 2>&1 \
  | grep "^.*FAIL.*Taskomatic service is running (sat5_taskomatic_running)$"
[ $? -ne 0 ] && bye "FAIL: Even with '--force' taskomatic check was not ran" 1
set -o pipefail
set -e

echo "PASS"
