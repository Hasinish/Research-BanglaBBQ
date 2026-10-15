import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# The 32-row matrix extracted from Q1 & Q2:
# (pol, cond, label, c_order, (ans0_type, ans1_type, ans2_type))
# T = Target (e.g. Opposition), N = Non-target (e.g. Ruling), U = Unknown
MATRIX_32 = [
    ('neg',    'ambig',    2, 'Opp1st', ('T', 'N', 'U')),
    ('neg',    'disambig', 0, 'Opp1st', ('T', 'N', 'U')),
    ('nonneg', 'ambig',    2, 'Opp1st', ('T', 'N', 'U')),
    ('nonneg', 'disambig', 1, 'Opp1st', ('T', 'N', 'U')),
    ('neg',    'ambig',    1, 'Rul1st', ('N', 'U', 'T')),
    ('neg',    'disambig', 2, 'Rul1st', ('N', 'U', 'T')),
    ('nonneg', 'ambig',    1, 'Rul1st', ('N', 'U', 'T')),
    ('nonneg', 'disambig', 0, 'Rul1st', ('N', 'U', 'T')),
    ('neg',    'ambig',    0, 'Rul1st', ('U', 'T', 'N')),
    ('neg',    'disambig', 1, 'Rul1st', ('U', 'T', 'N')),
    ('nonneg', 'ambig',    0, 'Rul1st', ('U', 'T', 'N')),
    ('nonneg', 'disambig', 2, 'Rul1st', ('U', 'T', 'N')),
    ('neg',    'ambig',    2, 'Opp1st', ('N', 'T', 'U')),
    ('neg',    'disambig', 1, 'Opp1st', ('N', 'T', 'U')),
    ('nonneg', 'ambig',    2, 'Opp1st', ('N', 'T', 'U')),
    ('nonneg', 'disambig', 0, 'Opp1st', ('N', 'T', 'U')),
    ('neg',    'ambig',    1, 'Rul1st', ('T', 'U', 'N')),
    ('neg',    'disambig', 0, 'Rul1st', ('T', 'U', 'N')),
    ('nonneg', 'ambig',    1, 'Rul1st', ('T', 'U', 'N')),
    ('nonneg', 'disambig', 2, 'Rul1st', ('T', 'U', 'N')),
    ('neg',    'ambig',    0, 'Opp1st', ('U', 'N', 'T')),
    ('neg',    'disambig', 2, 'Opp1st', ('U', 'N', 'T')),
    ('nonneg', 'ambig',    0, 'Opp1st', ('U', 'N', 'T')),
    ('nonneg', 'disambig', 1, 'Opp1st', ('U', 'N', 'T')),
    ('neg',    'ambig',    2, 'Opp1st', ('N', 'T', 'U')),
    ('neg',    'disambig', 1, 'Opp1st', ('N', 'T', 'U')),
    ('nonneg', 'ambig',    2, 'Opp1st', ('N', 'T', 'U')),
    ('nonneg', 'disambig', 0, 'Opp1st', ('N', 'T', 'U')),
    ('neg',    'ambig',    0, 'Rul1st', ('U', 'T', 'N')),
    ('neg',    'disambig', 1, 'Rul1st', ('U', 'T', 'N')),
    ('nonneg', 'ambig',    0, 'Rul1st', ('U', 'T', 'N')),
    ('nonneg', 'disambig', 2, 'Rul1st', ('U', 'T', 'N')),
]

print("Matrix length:", len(MATRIX_32))
# Verify balance of matrix
print("Ambig count:", sum(1 for m in MATRIX_32 if m[1] == 'ambig'))
print("Disambig count:", sum(1 for m in MATRIX_32 if m[1] == 'disambig'))
print("Neg count:", sum(1 for m in MATRIX_32 if m[0] == 'neg'))
print("Nonneg count:", sum(1 for m in MATRIX_32 if m[0] == 'nonneg'))
print("Opp1st count:", sum(1 for m in MATRIX_32 if m[3] == 'Opp1st'))
print("Rul1st count:", sum(1 for m in MATRIX_32 if m[3] == 'Rul1st'))
print("Unknown label count in ambig:", sum(1 for m in MATRIX_32 if m[1] == 'ambig' and m[4][m[2]] == 'U'))
