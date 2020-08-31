#!/usr/bin/env python3

import logging
import config
from instapaper_lib import Instapaper
from evernote_lib import Evernote
from xml.sax.saxutils import escape
import time
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError



class Instapaper_to_evernote():


    def __init__(self, user):

        logging.info("Synchroniser:: Instance created")

        self.INSTAPAPER_SYNC_LIMIT = config.INSTAPAPER_SYNC_LIMIT

        try:

            self.db_connection = psycopg2.connect(  host=config.db_host,
                                                    port = config.db_port,
                                                    dbname=config.db_name, 
                                                    user=config.db_user,
                                                    password=config.db_password)

            logging.info("Synchroniser:: connected to database")

        except Exception as error_message:

            print("Unable to connect to database :: %s" % error_message)
            exit()



    def __del__(self):

        if(self.db_connection):

            self.db_connection.close()   



    def setup_instapaper(self, username, password):

        logging.info("Synchroniser:: Setting up instapaper")

        self.instapaper_instance = Instapaper(config.instapaper_consumer_id, config.instapaper_consumer_secret)
        self.instapaper_instance.login(username, password)

        logging.info("Synchroniser:: Instapaper Setup Complete")



    def setup_evernote(self, oauth_token):

        logging.info("Synchroniser:: Setting up evernote")
 
        self.evernote_instance = Evernote(config.evernote_client_key, config.evernote_client_secret)
        self.evernote_instance.login(oauth_token)

        logging.info("Synchroniser:: Evernote Setup Complete")



    def run_sync(self):

        highlights = self.instapaper_instance.formulate_highlights(self.INSTAPAPER_SYNC_LIMIT)


        for highlight in highlights:

            if( self.check_already_syncd(highlight['bookmark_id']) ):

                logging.info("Already synchd, skipping: %s" % highlight['title'])
                continue

            else:

                self.save_article_to_evernote(highlight, 'Articles')

                new_sync_marker = { "from": "instapaper",
                                    "to": "evernote",
                                    "unique_id": highlight['bookmark_id'],
                                    "unique_id_type" : 'bookmark_id'}

                self.db_collection.insert_one(new_sync_marker)
                


    def check_already_syncd(self, identifier):

        logging.info("Checking if %s is already synchd" % identifier)

        cursor = self.db_connection.cursor()
        query = "select * from sync_instapaper_evernote"
        cursor.execute(query)

        results = cursor.fetchall() 

        exists = False

        for row in results:
            if (identifier == row[2]):
                exists = True

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
        content += '<div> <span style="font-weight:bold;">Highlights</span></div><br/>'
        content += highlights
        content += '</en-note>'

        # Create note

        notebook_guid = self.evernote_instance.get_notebook_guid(notebook)

        self.evernote_instance.create_note(title, content, notebook_guid)



if __name__ == "__main__":
    
    print("---- synchronise instapaper to evernote ---- ")

    logging.basicConfig(level=logging.INFO)

    synchroniser = Instapaper_to_evernote("toby")
    synchroniser.setup_instapaper(config.instapaper_username, config.instapaper_password)
    synchroniser.setup_evernote(config.evernote_oauth_token)

    while True:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        print("%s :: Synchronising Instapaper to Evernote" % current_time)
        synchroniser.run_sync()

        time.sleep(1800) # 1800 = 30mins, 3600 = 1 hr