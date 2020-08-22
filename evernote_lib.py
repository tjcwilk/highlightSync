#!/usr/bin/env python3

from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
from urllib.parse import urlsplit, parse_qs
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import logging
import secrets


class Evernote:

    def __init__(self, client_key, client_secret):

        logging.info("Client Key and credential set")
        self.CLIENT_KEY = client_key
        self.CLIENT_SECRET = client_secret

        self.oauth_request_token = False
        self.oauth_request_secret = False


        self.oauth_verifier = False



    def login(self):

        # Follow the OAuth 1.0 flow

        # 1 - Get a temporary oAuth Credential

        self.get_request_token(self.CLIENT_KEY, self.CLIENT_SECRET)

        # 2 - Obtain authorization from user, with the temporary oauth credential

        self.get_user_authorization()

        # 3 - Exchange request token and user verification token for access tokens

        self.get_access_token()




    def get_request_token(self, client_key, client_secret):
        
        logging.info("Getting OAuth request keys")

        callback_url = 'http://localhost:8080'
        temporary_credential_url_prod = "https://www.evernote.com/oauth"
        temporary_credential_url_sandbox = "https://sandbox.evernote.com/oauth"

        try:

            oauth = OAuth1(client_key, 
                            client_secret=client_secret, 
                            callback_uri=callback_url, 
                            signature_method=u'HMAC-SHA1', 
                            signature_type=u'query')

            response = requests.get(temporary_credential_url_sandbox, auth=oauth)

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

        logging.info("Getting User OAuth authorization permissions")

        authorization_url_sandbox = "https://sandbox.evernote.com/OAuth.action?oauth_token=%s" % (self.oauth_request_token)
        authorization_url_production = "https://www.evernote.com/OAuth.action?oauth_token=%s" % (self.oauth_request_token)


        print('Please authorize this application, by visiting %s' % authorization_url_sandbox)
        redirect_response = input('Paste the full redirect URL here: ')

        params = parse_qs(redirect_response)

        print(params)
        
        if 'oauth_verifier' in params:

            logging.info("User sucessfully authorised oauth flow")
            self.oauth_verifier = params['oauth_verifier'][0]

            return True

        else:

            logging.error("User OAuth authorisation failed")
            return False



    def get_access_token(self):

        logging.info("getting OAuth access token")

        url_sandbox = "https://sandbox.evernote.com/oauth"

        oauth = OAuth1( self.CLIENT_KEY,
                        client_secret=self.CLIENT_SECRET,
                        resource_owner_key=self.oauth_request_token,
                        resource_owner_secret=self.oauth_request_secret,
                        verifier=self.oauth_verifier,
                        signature_method=u'HMAC-SHA1', 
                        signature_type=u'query')

        response = requests.get(url=url_sandbox, auth=oauth)

        if(response.status_code == 200):

            params = parse_qs( response.content.decode('UTF-8') )

            self.oauth_access_token = params['oauth_token'][0]
            self.edam_shard = params['edam_shard'][0]
            self.edam_userId = params['edam_userId'][0]
            self.edam_expires = params['edam_expires'][0]
            self.edam_noteStoreUrl = params['edam_noteStoreUrl'][0]

            logging.info("Successfully obtained OAuth access tokens")

            return True

        else:

            logging.error("Unable to obtain OAuth access tokens")
            return False


    def connect_evernote(self, oauth_token):

        if(oauth_token):
            
            # TODO - check validity of the oauth token, and if invalid initiate
            # the oauth flow to get a new one.

            self.oauth_access_token = oauth_token

        if(self.oauth_access_token):

            self.evernote_client = EvernoteClient(token=self.oauth_access_token, sandbox=True, china=False)
            self.evernote_user_store = self.evernote_client.get_user_store()
            self.evernote_note_store = self.evernote_client.get_note_store()

        else:
            self.login()


    def list_notesbooks(self):
        
        # List all of the notebooks in the user's account
        notebooks = self.evernote_note_store.listNotebooks()
        print("Found ", len(notebooks), " notebooks:")

        for notebook in notebooks:
            print("  * ", notebook.name)


if __name__ == "__main__":

    print("---- Evernote ---- ")

    logging.basicConfig(level=logging.INFO)

    myEvernote = Evernote(secrets.evernote_client_key, secrets.evernote_client_secret)

    myEvernote.connect_evernote(secrets.evernote_oauth_token)
    myEvernote.list_notesbooks()
