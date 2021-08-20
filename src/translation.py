# standard
import gettext
# internal
from src import settings as s


# get current language
current_lang = s.LOCALE_LANGUAGES[s.get('general')['language']]

# install current language
lang = gettext.translation(s.LOCALE_DOMAIN, localedir=s.LOCALE_DIR, languages=[current_lang])
lang.install()


# create interface
_ = lang.gettext
