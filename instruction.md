# Billing Processor Bug Fix

A legacy billing processor binary at `/app/billing_processor` reads a binary
transaction log and outputs per-customer net totals (charges minus refunds/credits).

## The Bug

The program produces **incorrect totals**: refund/credit transactions (negative amounts)
appear as large positive charges instead of being subtracted from the customer balance.

For example, a $15.00 refund stored as `-1500` cents is processed as a `$640.36` charge.

**The source code is not available.** You must diagnose the root cause in the binary
and fix it.

## Transaction File Format

`/app/transactions.bin` contains fixed-size 10-byte records (little-endian):

| Offset | Size | Type     | Description                                    |
|--------|------|----------|------------------------------------------------|
| 0      | 4    | uint32_t | Customer ID                                    |
| 4      | 2    | int16_t  | Amount in cents (signed: negative = refund)    |
| 6      | 4    | uint32_t | Reserved / padding                             |

## Required Output

Run the fixed binary and save output to `/app/output.txt`:

```
CUST_001: <net_cents>
CUST_002: <net_cents>
```

One line per customer, sorted by customer ID ascending. Net total = sum of all
charges minus all refunds for that customer.

## Steps

1. Investigate the binary at `/app/billing_processor`
2. Diagnose and fix the signedness bug
3. Run: `/app/billing_processor /app/transactions.bin /app/output.txt`
4. Verify the output looks correct (refunds should reduce totals, not inflate them)

You have 3600 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
