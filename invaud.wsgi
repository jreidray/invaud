#!usr/local/bin/python3

import sys
import logging
from os import getenv
from dotenv import load_dotenv
from webapp import startServer

load_dotenv()
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, getenv('ROOT_DIR'))

application = startServer(
    rootDir = getenv('ROOT_DIR'),
    dataDir = getenv('DATA_DIR'),
    SECRET_KEY = getenv('SECRET_KEY'),
    username = getenv('USERNAME'),
    password = getenv('PASSWORD')
)