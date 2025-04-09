import os
import re

import polib
from django.conf import settings
from django.core.management.commands import makemessages

from googletrans import Translator
import asyncio


class Command(makemessages.Command):
    """
        python manage.py make_messages -l en -d djangojs --ignore=*.build.js
    """

    msgmerge_options = ["-q", "--backup=none", "--previous", "--update", "--no-fuzzy-matching", "--no-location"]
    # translator = Translator()
    RE_PATTERN = r'\{\{?[%\s\S]*?\}\}?|\%\([^\)]*\)[ds]?'

    async def translate_list(self, untranslated_list, dest):
        async with Translator() as translator:
            translations = await translator.translate(untranslated_list, dest=dest)
            return translations

    @staticmethod
    def get_path_map(selected_locale, domain) -> dict:
        path_map = {}
        for locale in selected_locale:
            for path in settings.LOCALE_PATHS:
                path_map.update({os.path.join(path, f'{locale}/LC_MESSAGES/{domain}.po'): locale})
        return path_map

    def po_translate(self, po_file, locale):
        untranslated_list = [entry.msgid for entry in po_file.untranslated_entries()]
        translated_list = asyncio.run(self.translate_list(untranslated_list, locale))

        for entry, translated in zip(po_file.untranslated_entries(), translated_list):
            variables_msgid = re.findall(self.RE_PATTERN, entry.msgid)
            is_msgid_starts_with_newline = entry.msgid.startswith("\n")
            is_msgid_end_with_newline = entry.msgid.endswith("\n")

            if not variables_msgid:
                entry.msgstr = translated.text
            else:
                variables_msgstr = re.findall(self.RE_PATTERN, translated.text)

                for var_msgstr, var_msgid in zip(variables_msgstr, variables_msgid):
                    translated.text = translated.text.replace(var_msgstr, var_msgid)
                    entry.msgstr = translated.text

            if is_msgid_starts_with_newline:
                entry.msgstr = "\n" + entry.msgstr
            if is_msgid_end_with_newline:
                entry.msgstr = entry.msgstr + "\n"

        po_file.save()

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--no-clear-fuzzy',
            dest='no_clear_fuzzy',
            help='Leaves the translation flagged as fuzzy',
            action='store_true'
        )

        parser.add_argument(
            "--no-translate",
            dest="no_translate",
            help="Don't add automatic translation",
            action="store_true"
        )

    def handle(self, *args, **options):
        res = super().handle(*args, **options)
        no_clear_fuzzy = options.pop('no_clear_fuzzy')
        no_translate = options.pop('no_translate')
        selected_locale = options.get('locale')
        domain = options.get('domain')
        path_map = self.get_path_map(selected_locale, domain)

        for path, locale in path_map.items():
            po_file = polib.pofile(path)

            # убираем fuzzy
            if not no_clear_fuzzy:
                for entry in po_file.fuzzy_entries():
                    entry.flags.remove('fuzzy')
                po_file.save()

            # добавляем перевод
            if not no_translate:
                self.po_translate(po_file, locale)

        return res
