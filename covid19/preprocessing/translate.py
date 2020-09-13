import pandas as pd
import pycountry
import gettext


class CountryTranslator:
# Ne traduit que de l'anglais vers un autre language
    def __init__(self, domain="iso3166", language="fr"):
        self.language = language
        self.domain = domain
        self.lang = gettext.translation(self.domain, pycountry.LOCALES_DIR, languages=[self.language])
        self.lang.install()

    def translate(self, country):
        yield _(country)
