"""Checks availability of infoabanner, provides channelnumber, program title etc. displayed in infobanner"""
import stbt

class Infobanner(stbt.FrameObject):
    """A class which checks if the Infobanner is shown on screen
    and provides with infobanner specific data"""

    @property
    def is_visible(self):
        return bool(stbt.match("images/dtv/infobanner_whiteline.png", frame=self._frame))

    @property
    def channelnumber(self):
        #TO DO:
        return "channelnumber"

