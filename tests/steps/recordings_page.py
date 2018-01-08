from time import sleep

import stbt
import ocr_utils



class RecordingsPage(stbt.FrameObject):
    """A class which checks if Recordings page is shown on screen
    and provides with Recordings related data"""
    recordings_options = ["alle", "korte termijn", "lange termijn"]
    @property
    def is_visible(self):
        return bool(stbt.match("images/recordingsPage/myLibraryTitle.png", frame=self._frame)) and  bool(stbt.match("images/recordingsPage/recordingsPage.png", frame=self._frame))


    @property
    def selection(self):
        recordings_options = self.recordings_options
        current_selection_text = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=30, y=184, right=263, bottom=291),
            mode=stbt.OcrMode.SINGLE_LINE,
            lang='nld',
            # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
            tesseract_user_words=recordings_options
        )

        for item in recordings_options:
            print "recordings option read as '%s'" % current_selection_text
            if ocr_utils .fuzzy_match(current_selection_text, item, 0.78):
                return item

