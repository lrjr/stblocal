"""Checks availability of popup, provides title and message of any popup"""
import stbt

class PopupBox(stbt.FrameObject):
    """A class which checks if any popup is shown on the screen
        and provides with message and options shown in the popup"""
    @property
    def is_visible(self):
        return bool(self._popup)

    @property
    def message(self):
        #TO DO:
        confirm_dialog = stbt.Region(x=self._popup.region.x, y=self._popup.region.y,
                                width=self._popup.region.width, height=self._popup.region.height)
        return stbt.ocr(region=confirm_dialog, frame=self._frame).replace('\n', ' ')



    @property
    def _popup(self):
        reference_popup={"images/popup/pop_up_confirm.png":"images/popup/tv_key_press_message_while_watching_on_demand.png",
                         "images/popup/start_from_beginning_popup_nl.png":"images/popup/start_from_beginning_message_nl.png",
                         "images/popup/record_for_more_than_60_days_nl.png":"images/popup/record_for_more_than_60_days_message_nl.png",
                         "images/popup/pvr_recording_7days_disappear_popup_nl.png":"images/popup/pvr_recording_7days_disappear_popup_message_nl.png",
                         "images/popup/stop_watching_recording_popup_nl.png":"images/popup/stop_watching_recording_popup_message_nl.png",
                         "images/programAlreadyRecording_popup.png":"images/programAlreadyRecording_popup.png",
                         "images/popup/OpnieuwBeginnenPopup.png":"images/popup/OpnieuwBeginnenPopup.png"}
        for popupImage,popUpMessage in reference_popup.iteritems():
            popup_match = stbt.match(popupImage, frame=self._frame)
            if popup_match:
                message_match = stbt.match(popUpMessage, frame=self._frame)
                if message_match:
                    return message_match
