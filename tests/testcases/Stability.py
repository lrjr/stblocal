from mainrunner import runner

"""Pressing PAUSE on play out of recording (Logo) test using STAF framework so that I should be able to pause play out of recording."""
def test_78231():
    runner.run("78231")

"""Pressing FORWARD from paused state (Black screen transition) test using STAF framework so that I should be able to forward the playout."""
def test_78243():
    runner.run("78243")

"""To check Age Rating Logo so it  is displayed at Bottom Right"""
def test_75740():
    runner.run("75740")