#!/usr/bin/env python3

import logging
import config
from instapaper_lib import Instapaper
from evernote_lib import Evernote
from xml.sax.saxutils import escape
import time
from datetime import datetime
import psycopg2


class Instapaper_to_evernote():

    ###############################################################################################
    #  Class Lifecycle
    ###############################################################################################

    def __init__(self, user_email):

        self.USER_EMAIL = user_email
        self.USER_ID = False
        self.INSTAPAPER_SYNC_LIMIT = config.INSTAPAPER_SYNC_LIMIT
        self.db_connection = False


    def __del__(self):
        self.db_disconnect()

    ###############################################################################################
    # Database Handlers
    ###############################################################################################

    def db_connect(self):

        try:

            self.db_connection = psycopg2.connect(  host=config.db_host,
                                                    port = config.db_port,
                                                    dbname=config.db_name, 
                                                    user=config.db_user,
                                                    password=config.db_password)

            logging.info("instapaper_to_evernote:: connected to database")

            user_id = self.lookup_userid(self.USER_EMAIL)

            if(user_id):
                self.USER_ID = user_id

            else:

                logging.error("instapaper_to_evernote:: Unable to find user, exiting")
                exit()

        except Exception as error_message:

            print("Unable to connect to database :: %s" % error_message)
            exit()


    def db_disconnect(self):
        if(self.db_connection):
            self.db_connection.close()  


    ###############################################################################################
    # Utility methods
    ###############################################################################################

    def lookup_userid(self, email):

        logging.info("Getting user ID for %s" % email)

        cursor = self.db_connection.cursor()

        query = """SELECT id from users where email=%s"""
        cursor.execute( query, (email,) )
        results = cursor.fetchone()

        if(results):
            logging.info("instapaper_to_evernote:: User found, %s has a UID of %s" % (email, results[0]))
            return results[0]
        else:
            return False


    ###############################################################################################
    # Synchronisation Handlers
    ###############################################################################################

    def run(self):

        print("---> Checking last %s articles" % self.INSTAPAPER_SYNC_LIMIT)

        highlights = self.instapaper_instance.formulate_highlights(self.INSTAPAPER_SYNC_LIMIT)

        for highlight in highlights:

            if( self.check_already_syncd(highlight['bookmark_id']) ):

                # Skip sync if contained in sync database

                logging.info("instapaper_to_evernote:: Already synchd, skipping: %s" % highlight['title'])
                continue

            else:

                # Save, and insert sync record into database

                print( "---> Saving new article: (%s) - %s" % (highlight['bookmark_id'], highlight['title']) )

                try:

                    # Create new note in evernote

                    self.save_article_to_evernote(highlight, 'Articles')

                    # Insert new database sync record

                    logging.info("instapaper_to_evernote:: inserting db sync record")

                    self.db_connect()
                    cursor = self.db_connection.cursor()

                    statement = """
                        INSERT INTO sync_instapaper_evernote (user_id, article_uid, article_title) VALUES
                        ( (SELECT id from users WHERE email=%s ), %s, %s );
                    """
                    values = (self.USER_EMAIL, highlight['bookmark_id'], highlight['title'])

                    cursor.execute( statement, values )
                    self.db_connection.commit()
                    count = cursor.rowcount

                    self.db_disconnect()

                    logging.info("instapaper_to_evernote:: Rows updated: %s" % count)

                except Exception as error:

                    logging.error("instapaper_to_evernote:: Problem inserting into sync database:: %s" % error)


    def check_already_syncd(self, identifier):

        logging.info("instapaper_to_evernote:: Checking if %s is already synchd" % identifier)

        self.db_connect()

        cursor = self.db_connection.cursor()
        query = "select * from sync_instapaper_evernote WHERE user_id=%s AND article_uid=%s"
        values = (self.USER_ID, str(identifier))
        cursor.execute(query, values)

        results = cursor.fetchone() 

        self.db_disconnect()

        if(results):
            return True
        else:
            return False


    ###############################################################################################
    # Instapaper Handlers
    ###############################################################################################

    def setup_instapaper(self, username, password):

        logging.info("instapaper_to_evernote:: Setting up instapaper")

        if(username and password):

            self.instapaper_instance = Instapaper(config.instapaper_consumer_id, config.instapaper_consumer_secret)
            self.instapaper_instance.login(username, password)

        else:

            logging.info("instapaper_to_evernote:: Getting instapaper credentials from database")

            self.db_connect()

            query = "SELECT instapaper_username, instapaper_password from instapaper_sessions WHERE user_id=%s"
            cursor = self.db_connection.cursor()
            cursor.execute(query, (self.USER_ID,))
            results = cursor.fetchone()

            logging.info("instapaper_to_evernote:: Instapaper credentials found in database: %s, %s" % (results[0], results[1]) )

            self.instapaper_instance = Instapaper(config.instapaper_consumer_id, config.instapaper_consumer_secret)
            self.instapaper_instance.login( results[0], results[1] )

            self.db_disconnect()


    ###############################################################################################
    # Evernote Handlers
    ###############################################################################################

    def setup_evernote(self, oauth_token):

        logging.info("instapaper_to_evernote:: Setting up evernote")

        if(oauth_token):
 
            logging.info("instapaper_to_evernote:: Getting evernote oauth token from config")
            self.evernote_instance = Evernote(config.evernote_client_key, config.evernote_client_secret)
            self.evernote_instance.login(oauth_token)

        else:

            logging.info("instapaper_to_evernote:: Getting evernote oauth token from database")

            self.db_connect()

            query = "SELECT session_token from evernote_sessions WHERE user_id=%s"
            cursor = self.db_connection.cursor()
            cursor.execute(query, (self.USER_ID,))
            results = cursor.fetchone()

            self.db_disconnect()

            logging.info("instapaper_to_evernote:: Session token for user found in database: %s" % results)

            self.evernote_instance = Evernote(config.evernote_client_key, config.evernote_client_secret)
            self.evernote_instance.login( results[0] )


            logging.info("instapaper_to_evernote:: Synchroniser:: Evernote Setup Complete")


    def save_article_to_evernote(self, article, notebook):

        logging.info("instapaper_to_evernote:: Saving to evernote - title: %s, (%d highlights)" % (article['title'],  len(article['highlights'])))

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
