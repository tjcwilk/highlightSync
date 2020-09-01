#!/usr/bin/env python3

import logging
import requests
import json
from requests_oauthlib import OAuth1
from urllib.parse import urlsplit, parse_qs
import config



class Instapaper():



    def __init__(self, consumer_id, consumer_secret): 

        logging.info("Instapaper:: Instance created")
        
        self.API_CONSUMER_ID = consumer_id
        self.API_CONSUMER_SECRET = consumer_secret

        self.oauth = False
        self.USER_OAUTH_TOKEN = False
        self.USER_OAUTH_SECRET = False
        


    def login(self, username, password):

        logging.info("Instapaper:: Logging in user: %s" % username)

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

            logging.info("Instapaper:: Logging Success")


        except Exception as error_message:

            print("Error: %s" % error_message)
       


    def check_login(self):

        logging.info("Instapaper:: checking login")

        url = "https://www.instapaper.com/api/1/account/verify_credentials"

        try:

            response = requests.post(url=url, auth=self.oauth)

            if(response.status_code == 200):

                logging.info("Instapaper:: User IS logged in")
                return True

            else:

                logging.info("Instapaper:: User IS NOT logged in")
                return False

        except Exception as error_message:

            print("Error %s" % error_message)



    def get_bookmarks(self, folder, limit):
         
        logging.info("Instapaper:: Fetching %d bookmarks from %s" % (limit, folder))

        url = "https://www.instapaper.com/api/1/bookmarks/list"

        try:

            response = requests.post(url=url, 
                                    auth=self.oauth,
                                    data ={ 'limit': limit, 
                                            'folder_id': folder})

            if(response.status_code == 200):

                json_data = json.loads( response.content.decode('UTF-8') )
                return(json_data)

            else:

                print("Error, getting bookmarks returned %d" % response.status_code)
                return False

        except Exception as error_message:

            print("Error %s" % error_message)



    def get_highlights(self, bookmark_id):

        logging.info("Instapaper:: fetching highlights for bookmark ID %d" % bookmark_id)

        url = "https://www.instapaper.com/api/1.1/bookmarks/%d/highlights" % bookmark_id

        try:

            response = requests.post(url=url, auth=self.oauth)

            if(response.status_code == 200):

                json_data = json.loads( response.content.decode('UTF-8') )
                return(json_data)

            else:

                print("error getting highlights, api returned %d" % response.status_code)
                return False


        except Exception as error_message:

            print("error: %s" % error_message)



    def formulate_highlights(self, check_count):

        logging.info("Instapaper:: Formulating highlights")

        aggregated_highlights = []

        bookmarks = self.get_bookmarks("archive", check_count)

        for bookmark in bookmarks:
  
            if "bookmark_id" not in bookmark:
                continue

            highlights = self.get_highlights(bookmark['bookmark_id'])
            
            if(highlights):

                new_highlights = []
                for highlight in highlights:
                    new_highlights.append({'highlight_id': highlight['highlight_id'],
                                            'highlight_text': highlight['text']})

                new_bookmark = {}
                new_bookmark['bookmark_id'] = bookmark['bookmark_id']
                new_bookmark['hash'] = bookmark['hash']
                new_bookmark['title'] = bookmark['title']
                new_bookmark['url'] = bookmark['url']
                new_bookmark['highlights'] = new_highlights

                aggregated_highlights.append(new_bookmark)


        return aggregated_highlights