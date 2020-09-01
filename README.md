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


# Usage

At the moment, this project is still in early stage development. At some point I will
make a decent client for it, but there isn't one available yet.

Feel free to make use of the modules in your own project. Alternativly, `cli_synchroniser.py` 
can be run from the command line, that runs the synchronisation operations. You will need to 
edit the file, and add your own synchronisation jobs in __main__ at the bottom.


# Roadmap

Highlight sources:
- [X] Instapaper
- [ ] Amazon Kindle
- [ ] GetPocket


Save locations:
- [X] Evernote
- [ ] Notion
- [ ] Roam Research


# Why do I spell synchronisation wrong?

Because i'm British.



