from mapper import yamlreader
import logging
from steps import common_utils, actionmenuoption_navigate


class stepresolver:
    """Resolve each step to corresponding classname.functionname(parameterlist) and execute it"""
    def __init__(self):
        """initialize YamlReader to load data from actionMapper.yaml"""
        self.yamlReader = yamlreader.yamlReader("actionMapper.yaml")


    def resolveStep(self,testStep,scope={}):
        """Excecute corresponding action for step"""
        print testStep
        print "resolveStep"
        step = testStep['step']
        print step
        self.resolve = testStep['resolve']
        print self.resolve
        actionKey = step.keys()[0]
        if self.resolve == True:
            print "**********"
            #Get action for key from yaml if resolve = True
            actionKey = self.yamlReader.getActionForKey(actionKey)
            print " step action from mapper :"
            print actionKey

        else:
            print "resolve false"
        params = step.values()[0]
        # TODO: Separate below functions into runner.py. Return value should be resolved step(params)
        functionCall = self.createFunctionCallStatement(actionKey, params, scope)
        dataReturned = self.excecuteAction(functionCall)
        return dataReturned


    def excecuteAction(self,functionCall=str):
        """Excecute the function call  string"""
        print "***********"
        print functionCall
        # TODO: Fix dynamic import
        # dynamic import
        # modulename = functionCall.split('.')[0]
        # print modulename
        # try:
        #     if self.resolve == True:
        #         # to import corresponding module to excecute function
        #         importstmt = "from steps import "+modulename
        #         print "module statement to excecute: "+importstmt
        #         exec importstmt
        #     else:
        #         print "RESOLVE FALSE"
        # except Exception, e:
        #     print "exception importing module :"+modulename
        #     print str(e)
        try:
            # excecuting step
            dataReturned = eval(functionCall)
            print dataReturned
            return dataReturned
        except Exception, e:
            logging.error("exception caught " + str(e))
            print functionCall
            #asserting if function call failed to excecute
            assert False,str(e)


    def createFunctionCallStatement(self, functionName, params, scope={}):
        """Create function call string to excecute the step"""
        if scope:
            scopeString = str(scope)
        else:
            scopeString = ""
        #get the parameter list for the function call
        functionCallStmt = functionName
        paramList = "("

        if params:
            paramIterator = params.iteritems()
            for key, value in paramIterator:
                paramList += str(key) + " = \"" +str(value) + "\","
                print paramList

        if scopeString != "":
            #attaching scope to param list
            paramList +="scope ="
            paramList += scopeString
        else:
            if params:
                paramList = paramList[:-1]

        paramList += ")"
        print "********"
        print paramList
        #attaching parameters to the function call
        functionCallStmt+=paramList

        if self.resolve == False:
            functionCallStmt = "common_utils." + functionCallStmt
        print("Function to excecute : " + functionCallStmt)
        return functionCallStmt
