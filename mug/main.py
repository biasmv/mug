#!/usr/bin/env python
import sys
from mug import verbs

HELP='''\
usage: mug <verb> [<args>]

Supported verbs are:

    status           Show working tree status
    commit           Record changes to the repository
    add              Add file contents to the index
'''
def main(argv=sys.argv):
    if len(argv) == 1:
        print HELP
        sys.exit(-1)
    verbs.execute(argv[1:])

if __name__ == '__main__':
    main()
