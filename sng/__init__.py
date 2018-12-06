"""Generate name proposals for companies, software, etc.
"""

# Importing a package is conceptually the same as importing that package's
# __init__.py file.
# It runs package initialization code.

# https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
# http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html

# You must explicitly import submodules:
from .Generator import Generator
from .Config import Config
from . import helpers

from .builtin_wordlists import show_builtin_wordlists, load_builtin_wordlist

__version__ = '0.3.2'
__all__ = ['Generator', 'Config', 'helpers',
           'show_builtin_wordlists', 'load_builtin_wordlist']
