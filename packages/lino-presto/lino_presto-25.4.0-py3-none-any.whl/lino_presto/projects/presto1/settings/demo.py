from ..settings import *


class Site(Site):
    languages = "en de fr"
    is_demo_site = True
    the_demo_date = 20170312
    default_ui = 'lino_react.react'


#    default_ui = 'lino_react.react'
#    default_ui = 'lino_extjs6.extjs'

SITE = Site(globals())

DEBUG = True
