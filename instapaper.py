#!/usr/bin/env python3

import requests
from requests_oauthlib import OAuth1
from urllib.parse import urlsplit, parse_qs
import secrets


class Instapaper():

    def __init__(self, consumer_id, consumer_secret): 
        
        self.API_CONSUMER_ID = consumer_id
        self.API_CONSUMER_SECRET = consumer_secret
        self.USER_OAUTH_TOKEN = False
        self.USER_OAUTH_SECRET = False
        

    def login(self, username, password):

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

            print(self.USER_OAUTH_TOKEN)
            print(self.USER_OAUTH_SECRET)

        except Exception as error_message:
            print("Error: %s" % error_message)
       



if __name__ == "__main__":

    print("---- Instapaper Sync ---- ")

    myInstapaper = Instapaper(secrets.instapaper_consumer_id, secrets.instapaper_consumer_secret)
    myInstapaper.login(secrets.instapaper_username, secrets.instapaper_password)