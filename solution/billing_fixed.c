/*
 * billing_fixed.c  —  ORACLE / reference solution
 *
 * Identical to billing.c with ONE fix:
 *   "unsigned short amount"  →  "int16_t amount"
 *
 * This causes the compiler to emit movswl (sign-extend) instead of
 * movzwl (zero-extend) when loading the 16-bit field, so negative
 * refund amounts are preserved correctly.
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

    uint32_t cust_id;
    int16_t  amount;    /* FIX: signed — movswl sign-extends correctly */
    uint32_t reserved;

    while (fread(&cust_id,  sizeof(uint32_t), 1, fin) == 1 &&
           fread(&amount,   sizeof(int16_t),  1, fin) == 1 &&
           fread(&reserved, sizeof(uint32_t), 1, fin) == 1) {

        if (cust_id < MAX_CUSTOMERS) {
            int32_t amt = amount; /* movswl: sign-extends → refunds are negative */
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
