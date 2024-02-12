#!/usr/bin/env python3
# -*- coding: cp1252 -*-
import sys
from icecream import ic

def get_argument():
    if len(sys.argv) < 2:
        print("Usage: python main.py <username>")
        return
    username = sys.argv[1]
    ic(username)

if __name__ == '__main__':
    get_argument()