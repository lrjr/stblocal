import stbt
import ocr_utils

class MainHubPage(stbt.FrameObject):
    """A class which checks if Main Hub page is shown on screen
    and provides with Hub related data"""
    hub_items = ["mijn bibliotheek", "televisie", "shop"]

    @property
    def is_visible(self):
        if(stbt.match("images/mainhub/home_breadcrumb_NL.png", frame=self._frame).match & stbt.match("images/mainhub/televisie_focusinshowcaseline_NL.png", frame=self._frame).match):
            return True
        else:
            return False

    @property
    def selection(self):
        hub_items = self.hub_items
        current_selection_text = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=360, y=520, right=640, bottom=570),
            mode=stbt.OcrMode.SINGLE_LINE,
            lang='nld',
            # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
            tesseract_user_words=hub_items
        )

        for item in hub_items:
            print "Main hub item read as '%s'" % current_selection_text
            if tests.steps.ocr_utils.fuzzy_match(current_selection_text, item, 0.78):
                return item