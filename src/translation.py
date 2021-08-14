# standard
import gettext
# internal
from src import settings as s


# get current language
general_settings = s.get('general')
current_lang = s.LOCALE_LANGUAGES.get(
    general_settings.get('language', ''),
    s.LOCALE_DEFAULT_LANG
)


# install current language
lang = gettext.translation(s.LOCALE_DOMAIN, localedir=s.LOCALE_DIR, languages=[current_lang])
lang.install()


# create interface
_ = lang.gettext
