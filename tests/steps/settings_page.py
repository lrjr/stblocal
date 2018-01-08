import stbt
import ocr_utils


class SettingsPage(stbt.FrameObject):
    """A class which checks if Settings page is shown on screen
    and provides with Settings related data"""
    settings_options = ["mijn account", "kinderslot", "aanbevelingen",
                                  "systeem", "zenders hernummeren", "mijn voorkeur",
                                  "beheer van de toestellen"]
    @property
    def is_visible(self):
        return bool(stbt.match("images/settings/settings_title_NL.png", frame=self._frame))

    @property
    def selection(self):
        settings_options = self.settings_options
        current_selection_text = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=360, y=383, right=885, bottom=420),
            mode=stbt.OcrMode.SINGLE_LINE,
            lang='nld',
            # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
            tesseract_user_words=settings_options
        )

        for item in settings_options:
            print "settings option read as '%s'" % current_selection_text
            if ocr_utils.fuzzy_match(current_selection_text, item, 0.78):
                return item

