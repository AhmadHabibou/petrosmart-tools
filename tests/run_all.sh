#!/bin/sh
# Runs every reference test. Requires Node.js 18 or later.
cd "$(dirname "$0")" || exit 1
fail=0
for t in test_*.js; do echo "== $t"; node "$t" || fail=1; done
exit $fail
