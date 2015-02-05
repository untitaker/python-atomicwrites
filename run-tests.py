#!/usr/bin/env python

import sys

if hasattr(sys, 'pypy_translation:info'):
    env_ident = 'pypy'
else:
    env_ident = 'py' + ''.join(map(str, sys.version_info[:2]))

from tox._cmdline import main
main(('-e', env_ident))
