#!/usr/bin/env python3

import logging
import secrets
from instapaper import Instapaper
from evernote_lib import Evernote
from pymongo import MongoClient
from xml.sax.saxutils import escape


class Synchroniser():


    def __init__(self, user, sync_from, sync_to):

        logging.info("Synchroniser:: Instance created")

        self.INSTAPAPER_SYNC_LIMIT = 20

        self.sync_from = sync_from
        self.sync_to = sync_to

        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client['sync_state']
        self.db_collection = self.db[user]



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



    def run_sync(self):

        if(self.sync_from=="INSTAPAPER" and self.sync_to=="EVERNOTE"):
            
            highlights = self.instapaper_instance.formulate_highlights(self.INSTAPAPER_SYNC_LIMIT)

            
            for highlight in highlights:

                if( self.check_already_syncd(highlight['bookmark_id']) ):

                    logging.info("Already synchd, skipping: %s" % highlight['title'])
                    continue

                else:

                    self.save_article_to_evernote(highlight, 'Articles')

                    new_sync_marker = { "from": self.sync_from,
                                        "to": self.sync_to,
                                        "unique_id": highlight['bookmark_id'],
                                        "unique_id_type" : 'bookmark_id'}

                    self.db_collection.insert_one(new_sync_marker)
                    


    def check_already_syncd(self, idenfitier):

        exists = self.db_collection.find_one({"unique_id": idenfitier})

        if(exists):
            return True
        else:
            return False



    def save_article_to_evernote(self, article, notebook):

        logging.info("Synchroniser:: Saving to evernote - title: %s, (%d highlights)" % (article['title'],  len(article['highlights'])))

        # Formulate evernote note

        title = article['title']

        url = "<div>Url: %s</div><br/><br/>" % ( escape(article['url']) )

        highlights = ''
        for highlight in article['highlights']:
            highlights += '<div>'
            highlights += escape(highlight['highlight_text'])
            highlights += '</div><br/>'


        content = '<?xml version="1.0" encoding="UTF-8"?>'
        content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        content += '<en-note>'
        content += url
        content += '<div>Highlights:</div><br/>'
        content += highlights
        content += '</en-note>'


        # Create note

        notebook_guid = self.evernote_instance.get_notebook_guid(notebook)

        self.evernote_instance.create_note(title, content, notebook_guid)





if __name__ == "__main__":
    
    print("---- synchroniser ---- ")

    logging.basicConfig(level=logging.INFO)

    instapaper_to_evernote = Synchroniser("toby", "INSTAPAPER", "EVERNOTE")
    instapaper_to_evernote.setup_instapaper(secrets.instapaper_username, secrets.instapaper_password)
    instapaper_to_evernote.setup_evernote(secrets.evernote_oauth_token)

    instapaper_to_evernote.run_sync()



    
