#!/usr/bin/env python
import sys
from mug import verbs

def main(argv=sys.argv):
    verbs.execute(argv[1:])

if __name__ == '__main__':
    main()
