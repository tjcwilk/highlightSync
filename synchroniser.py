#!/usr/bin/env python3

import logging
import secrets
from instapaper import Instapaper
from evernote_lib import Evernote


class Synchroniser():



    def __init__(self, sync_from, sync_to):

        logging.info("Synchroniser:: Instance created")

        self.sync_from = sync_from
        self.sync_to = sync_to



    def setup_instapaper(self, username, password):

        logging.info("Synchroniser:: Setting up instapaper")

        self.instapaper_instance = Instapaper(secrets.instapaper_consumer_id, secrets.instapaper_consumer_secret)
        self.instapaper_instance.login(username, password)

        logging.info("Synchroniser:: Instapaper Setup Complete")



    def setup_evernote(self, oauth_token):

        logging.info("Synchroniser:: Setting up evernote")
 
        self.evernote_instance = Evernote(secrets.evernote_client_key, secrets.evernote_client_secret)
        self.evernote_instance.login(oauth_token)

        logging.info("Synchroniser:: Evernote Setup Complete")



if __name__ == "__main__":
    
    print("---- synchroniser ---- ")

    logging.basicConfig(level=logging.INFO)

    instapaper_to_evernote = Synchroniser("INSTAPAPER", "EVERNOTE")

    instapaper_to_evernote.setup_instapaper(secrets.instapaper_username, secrets.instapaper_password)
    instapaper_to_evernote.setup_evernote(secrets.evernote_oauth_token)



    
