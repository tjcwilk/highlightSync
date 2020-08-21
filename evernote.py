#!/usr/bin/env python3

import logging

class Evernote:

    def __init__(self):
        logging.info('Evernote Class Created')


if __name__ == "__main__":

    print("---- Evernote ---- ")

    logging.basicConfig(level=logging.INFO)

    myEvernote = Evernote()