#!/usr/bin/env python

import sys

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = 'anonymous'
print(f'hello {name}')
