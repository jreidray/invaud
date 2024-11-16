#!usr/bin/python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/invaud/")

from webapp import startServer

application = startServer()