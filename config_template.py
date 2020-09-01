#!/usr/bin/env python3

#
# Synchroniser configration.
# 
# INTRUCTIONS -
#   Rename this file to config.py, and replace the config with your details.
#


# DATABASE (Postgresql)
db_host = "REPLACE_ME"
db_port = 5432
db_name = "REPLACE_ME"
db_user = "REPLACE_ME"
db_password = "REPLACE_ME"

#
# INSTAPAPER. Get your api key from https://www.instapaper.com/main/request_oauth_consumer_token
# if username & password is False, it will look up the creds in the database instead

INSTAPAPER_SYNC_LIMIT = 5
instapaper_consumer_id = "REPLACE_ME"
instapaper_consumer_secret = "REPLACE_ME"
instapaper_username = "REPLACE ME"
instapaper_password = "REPLACE_ME"

#
# EVERNOTE. Get your API key from https://dev.evernote.com/doc/
# if the oAuth token is false, it will look it up in the database instead

evernote_client_key = "REPLACE_ME"
evernote_client_secret = "REPLACE_ME"
evernote_oauth_token = False # Replace with your oAuth token. 