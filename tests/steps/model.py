class TestExecutionSteps:
    # The parameters to init needs to be the same as the json keys
    def __init__(self, resolve, step):
        self.resolve = resolve
        self.step = step

class Initializer:
    def __init__(self, testExecutionSteps):
        self.testExecutionSteps = testExecutionSteps

class Action:
    def __init__(self, testExecutionSteps):
        self.testExecutionSteps = testExecutionSteps

class Validator:
    def __init__(self, testExecutionSteps):
        self.testExecutionSteps = testExecutionSteps

class Steps:
    # def __init__(self, initializer, action, validator):
    #     self.initializer = initializer
    #     self.action = action
    #     self.validator = validator
    def __init__(self, testExecutionSteps):
        self.testExecutionSteps = testExecutionSteps
