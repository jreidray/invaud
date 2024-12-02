#!usr/bin/python

import sys
import logging
from os import getenv
from dotenv import load_dotenv
from webapp import startServer

load_dotenv()
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, getenv('ROOTDIR'))

application = startServer(
    rootDir = getenv('ROOTDIR'),
    SECRET_KEY = getenv('SECRET_KEY'),
    username = getenv('USERNAME'),
    password = getenv('PASSWORD')
)