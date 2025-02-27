AUTHOR = 'Me'
SITENAME = 'Quick Pose'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = False

TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''

IMAGES_PATH = f'{PATH}/images'
STATIC_PATHS = ['images', 'assets']

THEME_TEMPLATES_OVERRIDES = ['templates']

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

YADISK_PATH_PREFIX = 'disk:/'
YADISK_LISTINGS_PATH = ''
YANDEX_CLIENT_ID = ''
YANDEX_CLIENT_SECRET = ''
YANDEX_ACCESS_TOKEN = ''

from plugins.quick_poser import lightbox_generator

lightbox_generator.register()
PLUGINS = [lightbox_generator]
