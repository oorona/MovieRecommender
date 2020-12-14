#! /home/oorona/anaconda3/bin/python

import os
import psutil
import argparse
import sys

def memory_usage_psutil(pid):
    process = psutil.Process(pid)
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

if __name__ == "__main__":
    if len(sys.argv) ==1:
        for line in sys.stdin:
            pid=int(line)
    else:
        pid=int(sys.argv[1])

    print(memory_usage_psutil(pid))

