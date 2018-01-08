"""Handles the navigation in Main Settings page and navigation to other settings pages"""
import navigate, ocr_utils, settings_page
import stbt
from time import sleep

"""Navigates to an option in main settings page passed as string.
Returns True if it succeeds navigating to the settings option provided.
Returns False if it fails to find the settings option provided"""
def navigate_to_settingsoption(name):
    print "Looking for menu item '%s'" % name
    current_selection_text = stbt.ocr(
        region=stbt.Region(x=360, y=383, right=885, bottom=420),
        mode=stbt.OcrMode.SINGLE_LINE,
        lang='nld',
        # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
    )
    for _ in range(10):
        print "settings option read as '%s'" % current_selection_text
        if ocr_utils.fuzzy_match(current_selection_text, name, 0.78):
            return True
        stbt.press("KEY_DOWN")
        sleep(4)
    else:
        assert False, "Failed to find '%s' after pressing DOWN 10 times" % name

"""Navigates to settings page and then to audiolanguageandsubtitles settings page.
Returns True if succeeds in reaching the audiolanguageandsubtitles settings page.
Returns False if intended screen doesn't appear in the course of navigation"""
def nav_to_settings_audiolanguageandsubtitles():
    navigate.navigate_to("settings")
    if stbt.wait_until(lambda: settings_page.SettingsPage(), timeout_secs=3):
        navigate_to_settingsoption("mijn voorkeur")
        stbt.press("KEY_OK")
        if stbt.wait_until(lambda: stbt.match("images/settings/mypreference_title_NL.png"), timeout_secs=3):
            print "Launched My Preference Settings page"
            navigate_to_settingsoption("gesproken taal en ondertitels")
            stbt.press("KEY_OK")
            if stbt.wait_until(lambda: stbt.match("images/settings/audiolanguageandsubtitles_title_NL.png"), timeout_secs=3):
                print "Launched Audio language and Subtitles Settings page"
                return True
            else:
                assert False, "Failed to launch Audio language and Subtitles Settings page"
        else:
            assert False, "Failed to launch My Preference Settings page"
    else:
        assert False, "Failed to launch Settings page"
