#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | @AbirHasan2005

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os

def checkKey(dict, key):
  if key in dict.keys():
    return True
  else:
    return False


def delete_downloads():
  os.system('rm -rf /app/downloads/*')
