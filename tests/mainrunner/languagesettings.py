import gettext
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCALE_ROOT = PROJECT_ROOT.replace('mainrunner','locale')

class setlanguage:
    current_language = ""
    @staticmethod
    def __init__(language="nl_BE"):
        setlanguage.current_language=language
        APP = "messages"
        gettext.textdomain(APP)
        gettext.bindtextdomain(APP, LOCALE_ROOT)
        lang = gettext.translation(APP, LOCALE_ROOT, languages=[language], fallback= True)
        lang.install(APP,LOCALE_ROOT)
        _ = lang.gettext
