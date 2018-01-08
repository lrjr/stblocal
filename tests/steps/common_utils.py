"""This contains the generic utilities which is not specific to any particular feature"""

import stbt
import popup
import infobanner
from time import sleep
import actionmenuoption_navigate
import dtv_actionmenu_page
import mainhub_page

import recordings_page
import navigate
import json
import ast
from mapper import yamlreader
import logging
import sys
import ocr_utils

reload (sys)
sys.setdefaultencoding('utf8')
from mainrunner import languagesettings


class CommonUtils(object):
    popup = []
popup_messages = [
    "U kijkt naar een programma op aanvraag. Afspelen onderbreken?",
    "opnieuw beginnen",
    "Sommige opnames verdwijnen over minder dan 7 dagen.",
    "U kijkt naar een opname.Afspelen onderbroken",
    "Het is mogelijk om een opname",
    "Teletext is niet beschikbaar op dit kanaal."
    "Dit programma wordt reeds opgenomen."
    "Opnieuw beginnenPopup"
]
"""Turns ON the box if it is in OFF state.
Checks if the box is up and running, plays video and responds to keypresses."""
# TODO: Disable parental control
# TODO: Throw selected exception to stepBuilder to be thrown to STAF
def health_check(validate=True,scope=""):
    stbt.press("KEY_TV")
    dismissPopupIfPresent()
    stbt.press("KEY_INFO")
    if stbt.wait_until(lambda: infobanner.Infobanner()):
        print "Box is Up and responds to key presses"
        try:
            stbt.wait_for_motion()
            print "Video playback is present in Live TV"
            return {"status":True}
        except stbt.MotionTimeout:
            print "up key pressed"
            stbt.press("KEY_CHANNELUP")
            try:
                stbt.wait_for_motion()
                print "Video playback is present in Live TV"
                return {"status":True}
            except stbt.MotionTimeout:
                assert False, "Could not detect Video playback in Live TV"
    else:
        # TO DO else: <do one more IR event check>
        # if stbt.is_screen_black():
        stbt.press("KEY_MENU")
        if stbt.wait_until(lambda: not stbt.is_screen_black()):
            if stbt.wait_until(lambda: mainhub_page.MainHubPage()):
                sleep(1)
                print "Box is Up and responds to key presses"
                stbt.press("KEY_OK")
                if stbt.wait_until(lambda: not mainhub_page.MainHubPage()):
                    print "Dismissed Main Hub and tuned to live TV"
                else:
                    assert False, "Failed to tune to Live TV by OK press on Televisie from Main Hub"
                try:
                    stbt.wait_for_motion()
                    print "Video playback is present in Live TV"
                    return {"status":True}
                except stbt.MotionTimeout:
                    assert False, "Could not detect Video playback in Live TV"
            else:
                assert False, "Main_hub did not load. Health check failed"
        else:
            stbt.press("KEY_POWER")
            if stbt.wait_until(lambda: not stbt.is_screen_black(), timeout_secs=30):
                if stbt.wait_until(lambda: mainhub_page.MainHubPage()):
                    sleep(1)
                    print "Box is Up and responds to key presses"
                    stbt.press("KEY_OK")
                    if stbt.wait_until(lambda: not mainhub_page.MainHubPage()):
                        print "Dismissed Main Hub and tuned to live TV"
                    else:
                        assert False, "Failed to tune to Live TV by OK press on Televisie from Main Hub"
                    try:
                        stbt.wait_for_motion()
                        print "Video playback is present in Live TV"
                        return {"status":True}
                    except stbt.MotionTimeout:
                        assert False, "Could not detect Video playback in Live TV"
            else:
                assert False, "TV frozen with black screen"


"""Dismiss any popup which might appear in any screen."""
def dismissPopupIfPresent(scope={}):
    if popup.PopupBox():
        #TO DO check if it is safe to press OK to dismiss any popup which appears.
        stbt.press("KEY_OK")
    if stbt.wait_until(lambda: not popup.PopupBox()):
        return
    else:
        stbt.press("KEY_OK")
        assert stbt.wait_until(lambda: not popup.PopupBox())

def check_pip_window_shown():
    motionResult = stbt.wait_for_motion(
        timeout_secs=10,
        mask="images/pip_window_mask.png")
    if motionResult:
        print "Motion detected in region"
        return {"status":True}
    else:
        print "No Motion Detected"
        return {"status":False}

"""This method returns the name of the program from the info bar"""
def get_program_name_from_infobar():
    stbt.press("KEY_INFO")
    program_name=stbt.ocr(
        region=stbt.Region(x=316, y=627, right=1054, bottom=688))
    return program_name

"""This method validates if the video has been paused"""
def check_video_is_paused(scope={}):
    sleep(10)
    assert stbt.wait_until(lambda: stbt.match("images/recordingsPage/pauseImageDisplayed.png"))
    try:
        stbt.wait_for_motion()
        print "The video has not been paused"
        assert False
    except stbt.MotionTimeout:
        print "The video has been paused"


def checkposterimg():
    if actionmenuoption_navigate.navigate_to_actionmenuoption("Record"):
        print "matched"
    else:
        assert False, "Failed to "

def press_key(event,scope={}):
    print "Key press" + event
    stbt.press(event)
    sleep(2)



def play_live_tv(scope={}):
    """This test presses TV Button and if any popup comes presses OK.
    It validates live TV by checking for motion"""

    stbt.press('KEY_TV')  # Go to live TV
    sleep(3)
    if popup.PopupBox().is_visible:
        if popup.PopupBox().message in popup_messages:
            stbt.press('KEY_OK')
            assert stbt.wait_until(lambda: not popup.PopupBox().is_visible)

    if stbt.wait_for_motion():
        print "Motion Detected"
        return {"status":True}
    else:
        print "No motion detected"
        return {"status":False}


def check_for_motion(scope={}):
    dismissPopupIfPresent()
    if stbt.wait_for_motion():
        print "Motion Detected"
        return {"status":True}
    else:
        print "No motion detected"
        return {"status":False}


def check_icon_on_screen(icon,scope={},validate=True):
    coordinates = getCoordinatesOfIcon(icon)
    status= False
    try:
        if(stbt.wait_for_match(coordinates['image'],
                               region = stbt.Region(x=coordinates['x'],
                                                    y=coordinates['y'],
                                                    right=coordinates['right'],
                                                    bottom=coordinates['bottom']))):
            print "Icon present on screen"
            status=True
        else:
            print "Icon not present on screen"
            status = False
    except Exception ,e:
        print e
        print "Exception thrown"
    if validate:
        if status == False:
            assert "Icon not present on screen"
    else:
        return {"iconfound" : status}



def check_for_recording_icon(icon,scope={},validate=True):
    status= False
    dismissPopupIfPresent()
    coordinates = getCoordinatesOfIcon(icon)
    image = coordinates['image']
    x=coordinates['x']
    y=coordinates['y']
    right=coordinates['right']
    bottom=coordinates['bottom']
    imageRegion = stbt.Region(x,y,right,bottom)
    try:
        if(stbt.wait_for_match(image,region = stbt.Region(x,y,right,bottom))):
            print "Icon present on screen"
            status=True
        else:
            print "Icon not present on screen"
            status = False
    except Exception,e:
        print e
        print "Exception thrown"
    if validate:
        if status == False:
            assert "Icon not present on screen"
    else:
        return {"recordingIconfound" : status}

def getCoordinatesOfIcon(icon,scope={}):
    reader = yamlreader.yamlReader("coordinateMapper.yaml")
    icon_coordinates = dict
    icon_coordinates = reader.getActionForKey(icon)
    print ("icon_coordinates " + str(icon_coordinates))
    return icon_coordinates

def getProgram_Title(scope={}):
    print "Looking for title"
    stbt.press("KEY_INFO")
    stbt.wait_until(lambda: infobanner.Infobanner())
    sleep(2)
    current_selection_text = stbt.ocr(
        region=stbt.Region(x=317, y=633, right=838, bottom=683),
        mode=stbt.OcrMode.SINGLE_LINE,
        lang='nld',
        # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
    )
    return {"programTitle":current_selection_text}

def verify_recording_present(scope={},validate=True):
    status = False
    programTitle = scope['programTitle']
    recording_program_title = stbt.ocr(
        region=stbt.Region(x=595, y=277, right=938, bottom=312),
        mode=stbt.OcrMode.SINGLE_LINE,
        lang='nld',
        # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
    )
    print ("rec title" + str(recording_program_title))
    if ocr_utils .fuzzy_match(recording_program_title, programTitle, 0.78):
        print "Recording Present"
        status = True
    else:
        print "Recording is not available"
        status = False
    if validate:
        if status == False:
            assert "Icon not present on screen"
    else:
        return {"recordingfound" : status}


def verify_recording_page(scope={}):
    if stbt.wait_until(lambda: recordings_page.RecordingsPage()):
        return {"recordingPageAvailable":True}
    else:
        print "Recording Page is not available"
        return {"recordingPageAvailable":False}


"""Navigate through Zap list and find out a channel with Age Rating Logo"""
def tune_to_agerating_event(scope={}):
    coordinatesTen = getCoordinatesOfIcon("ageRating_icon_Ten")
    coordinatesTwelve = getCoordinatesOfIcon("ageRating_icon_Twelve")
    coordinatesSixteen = getCoordinatesOfIcon("ageRating_icon_Sixten")
    coordinatesEighteen = getCoordinatesOfIcon("ageRating_icon_Eighteen")
    try:
        for num in range(200):
            stbt.press("KEY_DOWN")
            sleep(2)
            tenAR = bool(stbt.match(coordinatesTen['image'],region = stbt.Region(x=coordinatesTen['x'],y=coordinatesTen['y'],right=coordinatesTen['right'],bottom=coordinatesTen['bottom'])))
            twelveAR = bool(stbt.match(coordinatesTwelve['image'],region = stbt.Region(x=coordinatesTwelve['x'],y=coordinatesTwelve['y'],right=coordinatesTwelve['right'],bottom=coordinatesTwelve['bottom'])))
            sixteenAR = bool(stbt.match(coordinatesSixteen['image'],region = stbt.Region(x=coordinatesSixteen['x'],y=coordinatesSixteen['y'],right=coordinatesSixteen['right'],bottom=coordinatesSixteen['bottom'])))
            eighteenAR = bool(stbt.match(coordinatesEighteen['image'],region = stbt.Region(x=coordinatesEighteen['x'],y=coordinatesEighteen['y'],right=coordinatesEighteen['right'],bottom=coordinatesEighteen['bottom'])))
            if (tenAR or twelveAR or sixteenAR or eighteenAR):
                stbt.press("KEY_OK")
                sleep(2)
                break
            else:
                print "Continue  through zap list"
        return {"status":True,"tenAR":tenAR,"twelveAR":twelveAR,"sixteenAR":sixteenAR,"eighteenAR":eighteenAR}
    except Exception,e:
        print "Couldnt find Channel with Age Rating"
        return {"status":False}


"""Verifies whether Age Rating logo is displayed at bottom right of the page"""
def verify_logo_position(scope={}):
    if scope['tenAR']:
        icon = "ageRating_logo_Ten"
    elif scope['twelveAR']:
        icon = "ageRating_logo_Twelve"
    elif scope['sixteenAR']:
        icon = "ageRating_logo_Sixteen"
    elif scope['eighteenAR']:
        icon = "ageRating_logo_Eighteen"
    stbt.press("KEY_INFO")
    check_icon_on_screen(icon)


def verify_recording_is_series(scope={}):
    if (bool(stbt.match("images/recordingsPage/seriesTitle.png"))):
        stbt.press("KEY_OK")
        sleep(3)


def resolve_image_path(path=str):
    """to support images in different language: resolves the path of image provided according to current language"""
    current_language = languagesettings.setlanguage.current_language
    path.replace('languageToBeReplaced',current_language)
