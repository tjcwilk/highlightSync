#!/usr/bin/env python3

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

import logging

class Evernote:

    def __init__(self):
        logging.info('Evernote Class Createdpi')


if __name__ == "__main__":

    print("---- Evernote ---- ")

    logging.basicConfig(level=logging.INFO)

    myEvernote = Evernote()