import time
import stbt


def test_channel_change_time():
    """
    Precondition: We're at live-tv
    """
    measure_channel_change_time(
        "KEY_CHANNELUP", "images/channel-change-mask.png")
    measure_channel_change_time(
        "KEY_CHANNELDOWN", "images/channel-change-mask.png")


def measure_channel_change_time(key, mask):
    import google

    # start timer after key press
    stbt.press(key)
    start_time = time.time()

    assert stbt.wait_until(lambda: stbt.is_screen_black(mask=mask)), \
        "Screen never went black"

    for frame, _ in stbt.frames(timeout_secs=30):
        if not stbt.is_screen_black(mask=mask, frame=frame):
            end_time = frame.time
            break
    else:
        assert False, "Channel change didn't complete after 30s"

    google.GoogleSheet().record_measurement(
        start_time, "channel_change", {"duration": end_time - start_time})
