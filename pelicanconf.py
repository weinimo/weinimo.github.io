#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Thomas Weininger'
SITENAME = u'weininger.net'
SITEURL = ''
#THEME = '/home/tom/workspace/pelican-themes/mg'
TIMEZONE = 'Europe/Monaco'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#~ LINKS =  (('Pelican', 'http://getpelican.com/'),
          #~ ('Python.org', 'http://python.org/'),
          #~ ('Jinja2', 'http://jinja.pocoo.org/'),
          #~ ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/weinimo'),)

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'pictures',
    'extra/robots.txt',
]

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
