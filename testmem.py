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
    print(memory_usage_psutil(int(sys.argv[1])))

