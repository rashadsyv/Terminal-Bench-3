#!/bin/bash
# Oracle solution: recompile from the fixed source and run it.
# Harbor mounts solution/ at /solution/ at runtime.
set -e

echo "[oracle] Compiling fixed binary..."
gcc -O0 -o /app/billing_processor /solution/billing_fixed.c

echo "[oracle] Running fixed binary..."
/app/billing_processor /app/transactions.bin /app/output.txt

echo "[oracle] Output:"
cat /app/output.txt
