# TODO: Remove this class. Can be done in runner.py itself
import json

class JsonParser:
    def parseJsonData(self, stepAsJson):
        print  stepAsJson['testSteps']
        return stepAsJson['testSteps']