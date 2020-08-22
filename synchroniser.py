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



    def run_sync(self):

        if(self.sync_from=="INSTAPAPER" and self.sync_to=="EVERNOTE"):
            
            highlights = self.instapaper_instance.formulate_highlights(2)
            
            for highlight in highlights:

                if( self.check_already_syncd() ):
                    logging.info("Already synchd, skipping: %s" % highlight[''])
                    continue
                else:

                    self.save_article_to_evernote(highlight, 'Articles')
                    


    def check_already_syncd(self):

        # TODO 
        return False



    def save_article_to_evernote(self, article, notebook):

        logging.info("Synchroniser:: Saving to evernote - title: %s, (%d highlights)" % (article['title'],  len(article['highlights'])))

        # Formulate evernote note

        title = article['title']

        url = "<div>Url: %s</div><br/><br/>" % (article['url'])

        highlights = ''
        for highlight in article['highlights']:
            highlights += '<div>'
            highlights += highlight['highlight_text']
            highlights += '</div><br/>'


        content = '<?xml version="1.0" encoding="UTF-8"?>'
        content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        content += '<en-note>'
        content += url
        content += highlights
        content += '</en-note>'


        # Create note

        notebook_guid = self.evernote_instance.get_notebook_guid(notebook)

        self.evernote_instance.create_note(title, content, notebook_guid)





if __name__ == "__main__":
    
    print("---- synchroniser ---- ")

    logging.basicConfig(level=logging.INFO)

    instapaper_to_evernote = Synchroniser("INSTAPAPER", "EVERNOTE")
    instapaper_to_evernote.setup_instapaper(secrets.instapaper_username, secrets.instapaper_password)
    instapaper_to_evernote.setup_evernote(secrets.evernote_oauth_token)

    instapaper_to_evernote.run_sync()



    
