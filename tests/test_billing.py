"""
test_billing.py  —  verifier for the billing_processor bug-fix task.

Reads /app/output.txt (the artifact produced by the agent's fix) and
verifies that per-customer net totals are correct.

Transaction data (from /app/transactions.bin):
  CUST_001:  +5000 - 1500 + 2000  =  5500 cents  ($55.00 net)
  CUST_002: +12000 - 3000 -  500  =  8500 cents  ($85.00 net)
  CUST_003:  +8500 - 1000         =  7500 cents  ($75.00 net)

The common failure mode for buggy output: refunds stored as negative int16_t
are zero-extended to large positives (e.g. -1500 → 64036), inflating totals
instead of reducing them.
"""
import os
import pytest

OUTPUT_FILE = "/app/output.txt"


def parse_output():
    """Parse CUST_NNN: <value> lines into a dict."""
    assert os.path.exists(OUTPUT_FILE), (
        f"{OUTPUT_FILE} not found — did the agent save the output?"
    )
    result = {}
    with open(OUTPUT_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": ", 1)
            assert len(parts) == 2, f"Unexpected output line format: {line!r}"
            result[parts[0]] = int(parts[1])
    return result


def test_output_file_exists():
    """Output file /app/output.txt must be present."""
    assert os.path.exists(OUTPUT_FILE), f"{OUTPUT_FILE} not found"


def test_all_customers_present():
    """All three customers must appear in the output."""
    data = parse_output()
    for cust in ("CUST_001", "CUST_002", "CUST_003"):
        assert cust in data, f"{cust} missing from output"


def test_customer_001_net_total():
    """
    CUST_001 transactions: +5000, -1500 (refund), +2000.
    Net = 5500 cents.  Buggy output would be ~71036 (refund zero-extended).
    """
    data = parse_output()
    assert data["CUST_001"] == 5500, (
        f"CUST_001: expected 5500, got {data.get('CUST_001')} "
        "(hint: refund of -1500 may have been treated as +64036)"
    )


def test_customer_002_net_total():
    """
    CUST_002 transactions: +12000, -3000 (refund), -500 (refund).
    Net = 8500 cents.  Buggy output would be ~139572.
    """
    data = parse_output()
    assert data["CUST_002"] == 8500, (
        f"CUST_002: expected 8500, got {data.get('CUST_002')}"
    )


def test_customer_003_net_total():
    """
    CUST_003 transactions: +8500, -1000 (refund).
    Net = 7500 cents.  Buggy output would be ~73036.
    """
    data = parse_output()
    assert data["CUST_003"] == 7500, (
        f"CUST_003: expected 7500, got {data.get('CUST_003')}"
    )
