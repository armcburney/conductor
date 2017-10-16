# Inefficiently finds primes within some range [start, end).

import sys
from math import sqrt, floor

start = 2
end = 3

if len(sys.argv) == 3:
    start = int(sys.argv[1])
    end = int(sys.argv[2])

if len(sys.argv) != 3 or start < 2 or end <= start:
    print('Usage: {0} start (>= 2) end (> start)'.format(sys.argv[0]))
    exit(1)

if start == 2:
    print(start)
if start % 2 == 0:
    start += 1

for num in range(start, end, 2):
    for den in range(3, floor(sqrt(num)) + 1, 2):
        if num % den == 0:
            break
    else:
        print(num)

