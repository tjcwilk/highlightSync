#!/usr/bin/env python3

import logging
import requests
from requests_oauthlib import OAuth1
from urllib.parse import urlsplit, parse_qs
import secrets



class Instapaper():



    def __init__(self, consumer_id, consumer_secret): 
        
        self.API_CONSUMER_ID = consumer_id
        self.API_CONSUMER_SECRET = consumer_secret

        self.oauth = False
        self.USER_OAUTH_TOKEN = False
        self.USER_OAUTH_SECRET = False
        


    def login(self, username, password):

        logging.info("Logging in user: %s" % username)

        url = "https://www.instapaper.com/api/1/oauth/access_token"

        auth = OAuth1(self.API_CONSUMER_ID, self.API_CONSUMER_SECRET)

        try:
            response = requests.post(url=url, 
                                auth=auth, 
                                data ={'x_auth_username': username, 
                                'x_auth_password': password, 
                                'x_auth_mode':'client_auth'})
            
            params = parse_qs(response.content.decode('UTF-8'))

            self.USER_OAUTH_TOKEN = params['oauth_token'][0]
            self.USER_OAUTH_SECRET = params['oauth_token_secret'][0]

            self.oauth = OAuth1(self.API_CONSUMER_ID,
                                self.API_CONSUMER_SECRET,
                                self.USER_OAUTH_TOKEN,
                                self.USER_OAUTH_SECRET)

            logging.info('User %s successfully logged in' % username )

        except Exception as error_message:

            print("Error: %s" % error_message)
       


    def check_login(self):

        logging.info('Checking oAuth login status')

        url = "https://www.instapaper.com/api/1/account/verify_credentials"

        try:

            response = requests.post(url=url, auth=self.oauth)

            if(response.status_code == 200):

                logging.info('User is logged in')
                return True

            else:

                logging.debug('User is not logged in')
                return False

        except Exception as error_message:

            print("Error %s" % error_message)



    def get_bookmarks(self, folder, limit):
         
        logging.info("Fetching %d bookmarks for %s" % (limit, folder))

        url = "https://www.instapaper.com/api/1/bookmarks/list"

        try:

            response = requests.post(url=url, 
                                    auth=self.oauth,
                                    data ={ 'limit': limit, 
                                            'folder_id': folder})

            if(response.status_code == 200):

                return( response.content.decode('UTF-8') )

            else:

                print("Error, getting bookmarks returned %d" % response.status_code)
                return False

        except Exception as error_message:

            print("Error %s" % error_message)




if __name__ == "__main__":

    print("---- Instapaper Sync ---- ")

    logging.basicConfig(level=logging.INFO)

    myInstapaper = Instapaper(secrets.instapaper_consumer_id, secrets.instapaper_consumer_secret)
    myInstapaper.login(secrets.instapaper_username, secrets.instapaper_password)
    
    print(myInstapaper.get_bookmarks("archive", 1))