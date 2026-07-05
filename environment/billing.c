/*
 * billing_processor.c
 *
 * Reads a binary transaction log and outputs per-customer net totals.
 *
 * Record format (10 bytes, little-endian):
 *   uint32_t  customer_id   [bytes 0-3]
 *   int16_t   amount_cents  [bytes 4-5]  (signed: negative = refund/credit)
 *   uint32_t  reserved      [bytes 6-9]
 *
 * Usage: billing_processor <input.bin> <output.txt>
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define MAX_CUSTOMERS 100

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: billing_processor <input.bin> <output.txt>\n");
        return 1;
    }

    long long totals[MAX_CUSTOMERS];
    int      seen[MAX_CUSTOMERS];
    memset(totals, 0, sizeof(totals));
    memset(seen,   0, sizeof(seen));

    FILE *fin = fopen(argv[1], "rb");
    if (!fin) { perror("fopen input"); return 1; }

    uint32_t      cust_id;
    unsigned short amount;   /* BUG: should be int16_t (signed short) */
    uint32_t      reserved;

    while (fread(&cust_id,  sizeof(uint32_t),       1, fin) == 1 &&
           fread(&amount,   sizeof(unsigned short),  1, fin) == 1 &&
           fread(&reserved, sizeof(uint32_t),        1, fin) == 1) {

        if (cust_id < MAX_CUSTOMERS) {
            int32_t amt = amount; /* movzwl: zero-extends → treats refunds as large positives */
            totals[cust_id] += (long long)amt;
            seen[cust_id] = 1;
        }
    }
    fclose(fin);

    FILE *fout = fopen(argv[2], "w");
    if (!fout) { perror("fopen output"); return 1; }

    for (int i = 0; i < MAX_CUSTOMERS; i++) {
        if (seen[i]) {
            fprintf(fout, "CUST_%03d: %lld\n", i, totals[i]);
        }
    }
    fclose(fout);
    return 0;
}
