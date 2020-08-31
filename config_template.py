#!/usr/bin/env python3

# This file holds config settings.

# DATABASE

mongo_url = 'mongodb://localhost:27017/'


# INSTAPAPER

INSTAPAPER_SYNC_LIMIT = 5 # How many articles to check

# Your instapaper client API Key, from https://www.instapaper.com/main/request_oauth_consumer_token
instapaper_consumer_id = "REPLACE_ME"
instapaper_consumer_secret = "REPLACE_ME"

# Your instapaper credentials. Their API doesn't implement oAuth properly, so you need these
instapaper_username = "REPLACE ME"
instapaper_password = "REPLACE_ME"


# EVERNOTE


# Your evernote client API key, from https://dev.evernote.com/doc/
evernote_client_key = "REPLACE_ME"
evernote_client_secret = "REPLACE_ME"

# If you have a long lasting evernote token, place it here. If not, the app will
# initiate the oauth flow, to get one. Then, you can paste it in.
evernote_oauth_token = False 