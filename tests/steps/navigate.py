import stbt

"""A dictionary that lists down the keypress list to navigate to the target screen"""
KeyPresses = {
    "settings" : ["KEY_MENU", "KEY_DOWN", "KEY_RIGHT", "KEY_RIGHT", "KEY_RIGHT", "KEY_OK"]
}

def navigate_to(context):
    for ctxt in KeyPresses:
        if ctxt == context:
            keypresslist = KeyPresses[context]
            break
    print "keypresslist '%s'" % keypresslist
    for key in keypresslist:
        print key
        stbt.press(key)
