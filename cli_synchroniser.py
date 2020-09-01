#!/usr/bin/env python3

import logging
import time
from datetime import datetime
from instapaper_to_evernote import Instapaper_to_evernote


class Synchroniser:

    def __init__(self):

        self.runners = []
        self.POLL_VALUE = 1800 # 1800 = 30mins, 3600 = 1 hr


    def add(self, runner):

        self.runners.append(runner)


    def start(self):

        while True:

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            print("-> sync started @ %s" % current_time)

            for synchroniser in self.runners:
                print("--> Synchroniser %s running for user: %s" %  ( synchroniser['type'], synchroniser['object'].USER_EMAIL))
                synchroniser['object'].run()

            print("-> sync complete.")

            time.sleep(1800)


if __name__ == "__main__":


    my_synchroniser = Synchroniser()

    toby_instapaper_to_evernote = Instapaper_to_evernote("toby@wilkins.io")
    toby_instapaper_to_evernote.setup_instapaper(False, False)
    toby_instapaper_to_evernote.setup_evernote(False)

    my_synchroniser.add(  { "type": "INSTAPAPER_TO_EVERNOTE", "object" : toby_instapaper_to_evernote } )

    my_synchroniser.start()
