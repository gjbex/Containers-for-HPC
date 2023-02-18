#!/usr/bin/env python

import argparse
import time

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='script that runs a while')
    arg_parser.add_argument('--max', type=int, default=60,
                            help='maximum number of seconds to run')
    arg_parser.add_argument('--file', help='file name to write the data to')
    options = arg_parser.parse_args()
    with open(options.file, 'w') as file: 
        for i in range(1, options.max + 1):
            print(f'value = {i}', file=file)
            time.sleep(1)
