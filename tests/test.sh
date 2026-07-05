#!/bin/bash
mkdir -p /logs/verifier
cd /tests
if python3 -m pytest test_billing.py -v; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi
exit 0
