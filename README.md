# Introduction

HighlightSync is a tool that can gather reading highlights collected from one service,
and save them in a different note taking tool.

This is particularly helpful when you read a lot of online digital content, but want
to collect it all together in your own central digital note taking library.

For example, I read a lot of technical articles using the reading service instapaper.
When I read, I highlight the parts that resonate with me. I like to bring these into my
central notes system evernote, so I can review, process and remember the content I read.


# Dependencies

- Tested on Ubuntu 20.04 and OSX 10.15 catalina
- Python3, and pip3
- A Postgresql database


# Installation

First clone this repository, and make sure you have python3 and pip3 installed.

I like to use a virtual environment. Create one with `virtualenv venv`, then activate
it using `source ./venv/bin/activate`.

Install the dependancies using `pip3 install -r requirements.txt`

rename the file `config_template.py` to `config.py`. Then, update it with
your own information. You will need some API keys from the service providers,
and a postgresql database to point the synchroniser at.



# Roadmap

Highlight sources:
- [X] Instapaper
- [ ] Amazon Kindle
- [ ] GetPocket


Save locations:
- [X] Evernote
- [ ] Notion
- [ ] Roam Research



