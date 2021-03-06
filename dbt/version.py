
import os, re
import argparse

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

REMOTE_VERISON_FILE = 'https://raw.githubusercontent.com/analyst-collective/dbt/master/.bumpversion.cfg'

def __parse_version(contents):
    matches = re.search(r"current_version = ([\.0-9]+)", contents)
    if matches is None or len(matches.groups()) != 1:
        return "???"
    else:
        version = matches.groups()[0]
        return version

def get_version():
    return __version__
    #dbt_dir = os.path.dirname(os.path.dirname(__file__))
    #version_cfg = os.path.join(dbt_dir, ".bumpversion.cfg")
    #if not os.path.exists(version_cfg):
    #    return "???"
    #else:
    #    with open(version_cfg) as fh:
    #        contents = fh.read()
    #        return __parse_version(contents)

def get_latest_version():
    f = urlopen(REMOTE_VERISON_FILE)
    contents = f.read()
    if hasattr(contents, 'decode'):
        contents = contents.decode('utf-8')
    return __parse_version(contents)

def not_latest():
    return """Your version of dbt is out of date! You can find instructions for upgrading here:
http://dbt.readthedocs.io/en/master/guide/upgrading/
"""

def get_version_string():
    return "installed version: {}\n   latest version: {}".format(installed, latest)

def get_version_information():
    basic = get_version_string()

    if is_latest():
        basic +='\nUp to date!'
    else:
        basic += '\n{}'.format(not_latest())

    return basic

def is_latest():
    return installed == latest

__version__ = '0.4.9'
installed = get_version()
latest = get_latest_version()


