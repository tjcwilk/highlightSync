#!/usr/bin/env python3

# This file holds the secret keys and passwords required for accounts.
# Rename this file to secrets.py, and then change the corresponding 
# fields to match your accounts.


# an instapaper API key for your application. Get this from 
# https://www.instapaper.com/main/request_oauth_consumer_token
instapaper_consumer_id = "REPLACE_ME"
instapaper_consumer_secret = "REPLACE_ME"

# This is the username and password for your instapaper account.
# The instapaper API incorrectly implements oAuth 1.0a. What it should
# do is support redirecting the user of your app into an authentication
# flow and pass pack the oauth session credentials. Instead, the API
# forces you to take the username and password from the user, and use ot
# to get the oauth credential. An issue ticket for this problem has already
# been submitted to instapaper. 
instapaper_username = "REPLACE ME"
instapaper_password = "REPLACE_ME"

# This is the Client consumer API key and secret, for your Evernote application.
# Request this at https://dev.evernote.com/doc/

evernote_client_key = "REPLACE_ME"
evernote_client_secret = "REPLACE_ME"
evernote_oauth_token = False  # If you have a valid oauth access token, you can place it here