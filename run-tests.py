#!/usr/bin/env python

import sys

if hasattr(sys, 'pypy_translation_info'):
    env_ident = 'pypy'
else:
    env_ident = 'py' + ''.join(map(str, sys.version_info[:2]))

from tox import cmdline
cmdline(('-e', env_ident))
