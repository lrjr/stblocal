"""Handles the navigation in Action Menu and Action Menu related operations"""
import stbt
import ocr_utils
from time import sleep
import dtv_actionmenu_page
import common_utils
from mainrunner import languagesettings

"""Navigates to the action menu option passed as string and returns True 
if it succeeds navigating to the input action menu option provided"""
def navigate_to_actionmenuoption(optionName, validate=True):

    optionName = _(optionName)
    print "Optionname to be searched : "+optionName
    print "Value of validate: "+ str(validate)
    optionFound = False
    error_message = "Failed to find '%s' after pressing DOWN 10 times" % optionName
    if stbt.wait_until(lambda: dtv_actionmenu_page.DTVActionMenuPage()):
        print "Looking for action menu option '%s'" % optionName
        sleep(2)
        option_list = []
        for num in range(11):
            current_selection_text = stbt.ocr(
                region=stbt.Region(x=373, y=467, right=925, bottom=505),
                mode=stbt.OcrMode.SINGLE_LINE,
                lang='nld',
                # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
            )
            if current_selection_text in option_list:
                print "All options iterated"
                print "No:of options : "+str(num)
                optionFound=False
                error_message = "Failed to find '%s'" % optionName
                break
            option_list.append(current_selection_text)
            print "nkjkjjj '%s'" % dtv_actionmenu_page.DTVActionMenuPage().selection
            print "action menu option read as '%s'" % current_selection_text
            if ocr_utils.fuzzy_match(current_selection_text, optionName, 0.78):
                print "Option " +optionName+ " found"
                optionFound=True
                error_message = ""
                break
            sleep(2)
            stbt.press("KEY_DOWN")
            sleep(4)

    else:
        optionFound=False
        error_message = "Failed to launch Action Menu"
    if validate:
        print "Validating step"
        print "optionFound : "+str(optionFound)
        if optionFound == False:
            assert optionFound, error_message
    else:

        returnvalue = {"optionFound": optionFound, "option_list":option_list, "error_message" : error_message}
        print "returning value from step navigate_to_actionmenuoption : "+ str(returnvalue)
        return returnvalue

"""Navigates to one among the displayed options in the stop recording confirmation page in Action Menu
and returns True if it succeeds navigating to the input(String) provided"""
def navigate_to_stoprecordingconfirmationoption(optionName):

    optionName = _(optionName)
    print "Looking for stop recording confirmation option '%s'" % optionName

    for _ in range(2):
        current_selection_text = stbt.ocr(
            region=stbt.Region(x=392, y=550, right=610, bottom=595),
            mode=stbt.OcrMode.SINGLE_LINE,
            lang='nld',
            # tesseract_config={'load_system_dawg':False, 'load_freq_dawg':False},
        )
        print "stop recording confirmation option read as '%s'" % current_selection_text
        if ocr_utils.fuzzy_match(current_selection_text, optionName, 0.78):
            sleep(2)
            return {"status":True}
        stbt.press("KEY_DOWN")
        sleep(4)
    else:
        assert False, "Failed to find '%s' after pressing DOWN 2 times" % optionName


"""Navigates to the action menu option passed as string until finding it in LiveTV by zapping channels
and returns True if it succeeds navigating to the input action menu option provided"""
def nav_to_actionmenuoption_untilfinding_dtv(optionName):
    for _ in range(5):
        optionDict = navigate_to_actionmenuoption(optionName,False)
        optionDict = dict(optionDict)
        if optionDict.get('optionFound') == True:
            print "channel with "+optionName+" found"
            common_utils.press_key("KEY_TV")
            break
        common_utils.press_key("KEY_TV")
        common_utils.press_key("KEY_CHANNELUP")
        common_utils.press_key("KEY_OK")
