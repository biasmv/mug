#!/usr/bin/env python
import sys
from mug import verbs

def main():
    verbs.execute(sys.argv[1:])

if __name__ == '__main__':
    main()
