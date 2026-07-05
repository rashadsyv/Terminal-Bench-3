"""
generate_transactions.py  —  creates /app/transactions.bin

Binary format per record (10 bytes, little-endian):
  uint32_t  customer_id    (4 bytes)
  int16_t   amount_cents   (2 bytes, signed: negative = refund)
  uint32_t  reserved       (4 bytes, always 0)

Expected correct net totals:
  CUST_001:  5000 - 1500 + 2000  =  5500
  CUST_002: 12000 - 3000 -  500  =  8500
  CUST_003:  8500 - 1000         =  7500
"""
import struct
import sys

RECORDS = [
    (1,  5000),   # customer 1: charge $50.00
    (1, -1500),   # customer 1: refund $15.00
    (2, 12000),   # customer 2: charge $120.00
    (2, -3000),   # customer 2: refund $30.00
    (3,  8500),   # customer 3: charge $85.00
    (1,  2000),   # customer 1: charge $20.00
    (2,  -500),   # customer 2: refund $5.00
    (3, -1000),   # customer 3: refund $10.00
]

output_path = sys.argv[1] if len(sys.argv) > 1 else "/app/transactions.bin"

with open(output_path, "wb") as f:
    for cust_id, amount in RECORDS:
        # '<IhI': little-endian, uint32 + int16 + uint32 = 10 bytes
        f.write(struct.pack("<IhI", cust_id, amount, 0))

print(f"Written {len(RECORDS)} records to {output_path}")
