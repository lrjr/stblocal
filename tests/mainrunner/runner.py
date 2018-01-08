import languagesettings
# set language to default
languagesettings.setlanguage()

import jsonparser
from stepresolver import stepbuilder
import requests
import json



# sample json received from STAF
dataJson = {"testSteps":[
    {"resolve":True,"step":{"stb_poweron":""}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_TV"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_OK"}}},
    {"resolve":True,"step":{"navigate_to_option_actionmenu":{"optionName" : "Record"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_OK"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_TV"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_OK"}}},
    {"resolve":True,"step":{"navigate_to_option_actionmenu":{"optionName" : "Stop Recording"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_TV"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_OK"}}},
    {"resolve":True,"step":{"navigate_to_option_actionmenu":{"optionName" : "Stop Recording"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_OK"}}},
    {"resolve":True,"step":{"select_option_in-confirmationPage":{"optionName" : "confirm"}}},
    {"resolve":True,"step":{"press_key":{"event" : "KEY_OK"}}},
    {"resolve":True,"step":{"navigate_to_option_actionmenu":{"optionName" : "Record"}}}
]}

dataJson78229 = {"testSteps":[{"resolve":true,"step":{"stb_poweron":{"validate":true}}},{"resolve":false,"step":{"press_key":{"event":"KEY_TV"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"navigate_to_option_actionmenu":{"optionName":"Record"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_TV"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"navigate_to_option_actionmenu":{"optionName":"Stop Recording"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_TV"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"navigate_to_option_actionmenu":{"optionName":"Stop Recording"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"select_option_in-confirmationPage":{"optionName":"confirm"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"navigate_to_option_actionmenu":{"optionName":"Record"}}}]}
dataJson2 = {"testSteps":[{"resolve":True,"step":{"get_program_title":{}}}]}
dataJson1 = json.loads("""{"testSteps":[{"resolve":true,"step":{"stb_poweron":{"validate":true}}},{"resolve":true,"step":{"move_to_liveTV":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_INFO"}}},{"resolve":true,"step":{"get_program_title":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_RECORD"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_INFO"}}},{"resolve":true,"step":{"match_recording_icon":{"icon":"recording_icon"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_PVR"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":false,"step":{"verify_recording_list_page":{}}},{"resolve":false,"step":{"verify_recording_is_present":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":false,"step":{"validate_video_playback":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_PAUSE"}}},{"resolve":false,"step":{"validate_pause_option":{}}},{"resolve":true,"step":{"match_icon":{"icon":"pause_icon"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_FASTFORWARD"}}},{"resolve":true,"step":{"match_icon":{"icon":"forward_icon"}}}]}""")


dataJson3 = json.loads("""{"testSteps":[{"resolve":true,"step":{"stb_poweron":{"validate":true}}},{"resolve":true,"step":{"move_to_liveTV":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_INFO"}}},{"resolve":true,"step":{"get_program_title":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_RECORD"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_GUIDE"}}},{"resolve":true,"step":{"match_recording_icon":{"icon":"recording_icon"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_PVR"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"verify_recording_list_page":{}}},{"resolve":true,"step":{"verify_recording_is_present":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"verify_recording_is_series":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_OK"}}},{"resolve":true,"step":{"validate_video_playback":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_PAUSE"}}},{"resolve":true,"step":{"validate_pause_option":{}}},{"resolve":true,"step":{"match_icon":{"icon":"pause_icon"}}},{"resolve":false,"step":{"press_key":{"event":"KEY_FASTFORWARD"}}},{"resolve":true,"step":{"match_icon":{"icon":"forward_icon"}}}]}""")



dataJson4 = json.loads("""{"testSteps":[{"resolve":true,"step":{"stb_poweron":{"validate":true}}},{"resolve":true,"step":{"move_to_liveTV":{}}},{"resolve":true,"step":{"tune_to_agerating_event":{}}},{"resolve":false,"step":{"press_key":{"event":"KEY_INFO"}}},{"resolve":true,"step":{"verify_logo_position":{}}}]}""")

def invokeParser(dataJson):
    print "inside invokeParser"
    parser = jsonparser.JsonParser()
    steps = parser.parseJsonData(dataJson)
    print "got steps"
    resolver = stepbuilder.stepresolver()
    scope = dict
    scope = {}
    for step in steps:
        print step
        valueReturned = resolver.resolveStep(step,scope)
        if valueReturned != None:
            scope.update(valueReturned)

def run(testcaseId):
    print "in run"
    #invoke STAF API to get the json
    # + testcaseId
    # requestString = "http://35.227.106.84:8081/api/testdata/7010"
    #requestString = "http://35.227.106.84:8081/api/testdata/" + testcaseId
    #response = requests.get(requestString, timeout=5,headers={"Authorization": "token QEJC-PYsuFN-IUowZT64Cj-btXU-KosC"})
    # print "The response is: %s" %response.content
    # invokeParser(response.content)
    invokeParser(dataJson78229)



"""if __name__ == '__main__':
    run()

    #TODO: Move the constants into a configuraion file
    requestString = "http://35.227.106.84:8081/api/testdata/" + testcaseId
    response = requests.get(requestString, timeout=10,headers={"Authorization": "token QEJC-PYsuFN-IUowZT64Cj-btXU-KosC"})
    print "The response is: %s" %response.content
    invokeParser(json.loads(response.content))"""



