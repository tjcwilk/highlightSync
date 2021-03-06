#!/usr/bin/env python3

from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
from urllib.parse import urlsplit, parse_qs
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import logging
import config


class Evernote:

    def __init__(self, client_key, client_secret):

        if not (config.EVERNOTE_SANDBOX):
            self.EVERNOTE_URL = "https://www.evernote.com"
        else:
            self.EVERNOTE_URL = "https://sandbox.evernote.com"

        logging.info("Evernote:: Instance Created")
        self.CLIENT_KEY = client_key
        self.CLIENT_SECRET = client_secret

        self.oauth_request_token = False
        self.oauth_request_secret = False


        self.oauth_verifier = False



    def login(self, oauth_token):

        logging.info("Evernote:: Logging in")

        if(oauth_token):

            logging.info("Evernote:: Using supplied OAuth key")

            # TODO - check validity of the oauth token, and if invalid initiate
            # the oauth flow to get a new one.

            self.oauth_access_token = oauth_token

            self.evernote_client = EvernoteClient(token=self.oauth_access_token, sandbox=config.EVERNOTE_SANDBOX, china=False)
            self.evernote_user_store = self.evernote_client.get_user_store()
            self.evernote_note_store = self.evernote_client.get_note_store()

            logging.info("Evernote:: Login Complete")

        else:

            logging.info("Evernote:: No OAuth Key, initiating authorisation flow")

            # Follow the OAuth 1.0 flow

            # 1 - Get a temporary oAuth Credential

            self.get_request_token(self.CLIENT_KEY, self.CLIENT_SECRET)

            # 2 - Obtain authorization from user, with the temporary oauth credential

            self.get_user_authorization()

            # 3 - Exchange request token and user verification token for access tokens

            self.get_access_token()

            self.evernote_client = EvernoteClient(token=self.oauth_access_token, sandbox=config.EVERNOTE_SANDBOX, china=False)
            self.evernote_user_store = self.evernote_client.get_user_store()
            self.evernote_note_store = self.evernote_client.get_note_store()

            logging.info("Evernote:: Login Complete")


    def get_request_token(self, client_key, client_secret):
        
        logging.info("Evernote:: Getting OAuth request keys")

        callback_url = 'http://localhost:8080'
        endpoint_url = "%s/oauth" % (self.EVERNOTE_URL)

        try:

            oauth = OAuth1(client_key, 
                            client_secret=client_secret, 
                            callback_uri=callback_url, 
                            signature_method=u'HMAC-SHA1', 
                            signature_type=u'query')

            response = requests.get(endpoint_url, auth=oauth)

            if(response.status_code == 200):

                params = parse_qs(response.content.decode('UTF-8'))

                self.oauth_request_token = params['oauth_token'][0]
                self.oauth_request_secret = params['oauth_token_secret'][0]

                return True

            else:

                return False

        except Exception as error_message:

                print("Error: %s" % error_message)
                return False



    def get_user_authorization(self):

        logging.info("Evernote:: Getting User OAuth authorization permission")

        endpoint_url =  "%s/OAuth.action?oauth_token=%s" % (self.EVERNOTE_URL, self.oauth_request_token)

        print('Please authorize this application, by visiting %s' % endpoint_url)
        redirect_response = input('Paste the full redirect URL here: ')

        params = parse_qs(redirect_response)

        print(params)
        
        if 'oauth_verifier' in params:

            logging.info("Evernote:: User successfully authorised oauth flow")
            self.oauth_verifier = params['oauth_verifier'][0]

            return True

        else:

            logging.error("Evernote:: User OAuth authorisation failed")
            return False



    def get_access_token(self):

        logging.info("Evernote:: getting OAuth access token")

        endpoint_url = "%s/oauth" % (self.EVERNOTE_URL)

        oauth = OAuth1( self.CLIENT_KEY,
                        client_secret=self.CLIENT_SECRET,
                        resource_owner_key=self.oauth_request_token,
                        resource_owner_secret=self.oauth_request_secret,
                        verifier=self.oauth_verifier,
                        signature_method=u'HMAC-SHA1', 
                        signature_type=u'query')

        response = requests.get(url=endpoint_url, auth=oauth)

        if(response.status_code == 200):

            params = parse_qs( response.content.decode('UTF-8') )

            self.oauth_access_token = params['oauth_token'][0]
            self.edam_shard = params['edam_shard'][0]
            self.edam_userId = params['edam_userId'][0]
            self.edam_expires = params['edam_expires'][0]
            self.edam_noteStoreUrl = params['edam_noteStoreUrl'][0]

            logging.info("Evernote:: Successfully obtained OAuth access tokens")
            print("----------------------\n")
            print(" Your API Access token is:")
            print("\t%s" % self.oauth_access_token)
            print("\n\n Copy/Paste this into your config file, to save it for next time\n")
            print("--------------------------\n\n")

            return True

        else:

            logging.error("Evernote:: Unable to obtain OAuth access tokens")
            return False


    def list_notesbooks(self):
        
        # List all of the notebooks in the user's account
        notebooks = self.evernote_note_store.listNotebooks()
        print("Found ", len(notebooks), " notebooks:")

        for notebook in notebooks:
            print("  * ", notebook.name)



    def create_note(self, title, content, notebook_guid):

        logging.info("Evernote:: Creating new evernote Note")

        note = Types.Note()
        note.title = title
        note.content = content

        if(notebook_guid):
            note.notebookGuid = notebook_guid

        self.evernote_note_store.createNote(note)


    def get_notebook_guid(self, notebook_name):

        notebooks = self.evernote_note_store.listNotebooks()
        notebook_guid = False

        for notebook in notebooks:
            if(notebook.name == notebook_name):
                notebook_guid = notebook.guid

        return notebook_guid