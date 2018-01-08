"""Tests for the home menu."""

import stbt
from stbt import wait_until


class HomeMenu(stbt.FrameObject):
    """A class that knows how to read the "home" UI (when you press KEY_MENU).

    For more information about stb-tester FrameObjects and how to test them see
    https://stb-tester.com/tutorials/using-frame-objects-to-extract-information-from-the-screen
    """

    @property
    def is_visible(self):
        return bool(stbt.match("images/home.png", frame=self._frame))

    @property
    def selection(self):
        current_selection_text = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=360, y=520, right=650, bottom=580))
        for item in ["mijn bibliotheek", "televisie", "shop"]:
            if current_selection_text.startswith(item):
                return item


def test_remote_control():
    """Simple test to see if the remote control is reliable.

    Presses left & right, and checks that each press has the necessary effect
    in the Home menu.
    """

    assert wait_until(lambda: not HomeMenu().is_visible)
    stbt.press("KEY_MENU")
    assert wait_until(lambda: HomeMenu().selection == "televisie")

    for _ in range(10):
        stbt.press("KEY_RIGHT")
        assert wait_until(lambda: HomeMenu().selection == "shop")
        stbt.press("KEY_LEFT")
        assert wait_until(lambda: HomeMenu().selection == "televisie")


