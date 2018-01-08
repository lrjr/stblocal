from encodings.punycode import selective_find
import yaml
import os

CURR_DIR = os.path.abspath(os.path.dirname(__file__))


class yamlReader:

    def __init__(self, filename, filePath=CURR_DIR):
        """Initialize data in yaml to dictionary
        :rtype: object
        """
        os.chdir(filePath)
        with open(filename, 'r') as stream:
            try:
                self.mapperDict = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def getActionForKey(self, key):
        """Returns value for given key from yaml file"""
        print "getActionForKey method called for key" + key
        try:
            stepAction = self.mapperDict[key]
            if stepAction == None:
                assert False,"Step Action not found for key : " +key
            else:
                return stepAction
        except Exception,e :
            #asserting if exception while getting value from yaml
            print e
            assert False,e


