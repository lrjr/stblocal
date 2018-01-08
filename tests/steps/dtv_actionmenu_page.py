import stbt
import ocr_utils

class DTVActionMenuPage(stbt.FrameObject):
    """A class which checks if DTV Action Menu page is shown on screen
    and provides with Action Menu related data"""
    # actionmenu_items = ["kijken", "pauzeren", "herstarten",
    #                  "opnemen", "opname stoppen", "serie opnemen",
    #                  "serieopname annuleren", "zendercatalogus", "ondertitels",
    #                  "gesproken taal en ondertitels", "gesproken taal"]
    actionmenu_items = [_("watch"), _("pause"), _("start over"),
                        _("record"), _("stop recording"), _("record series"),
                        _("cancel series recording"), _("channel catalog"), _("subtitles"),
                        _("channel language & subtitle"), _("primary audio")]
    @property
    def is_visible(self):
        if(stbt.match("images/dtv/television_breadcrumb_NL.png", frame=self._frame).match):
            return True
        else:
            return False

    @property
    def selection(self):
        actionmenu_items = self.actionmenu_items
        current_selection_text = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=360, y=548, right=855, bottom=663),
            mode=stbt.OcrMode.SINGLE_LINE,
            lang='nld',
            # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
            tesseract_user_words=actionmenu_items
        )

        for item in actionmenu_items:
            print "action menu option read as '%s'" % current_selection_text
            if ocr_utils.fuzzy_match(current_selection_text, item, 0.78):
                return item
