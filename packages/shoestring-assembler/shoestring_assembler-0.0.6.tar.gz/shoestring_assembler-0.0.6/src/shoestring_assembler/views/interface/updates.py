from enum import Enum

class Detail(Enum):
    ALWAYS = 0

    
    
    DEBUG = 5


class StageHeading:
    def __init__(self, stage):
        self.stage = stage


class StepHeading:
    def __init__(self, section):
        self.step = section


class InfoMsg:
    def __init__(self, content, detail_level=Detail.ALWAYS):
        self.content = content
        self.detail_level = detail_level


class WarningMsg:
    def __init__(self, content):
        self.content = content


class ErrorMsg:
    def __init__(self, content):
        self.content = content


class SuccessMsg:
    def __init__(self, content):
        self.content = content


class DebugLog:
    def __init__(self, content):
        self.content = content


class AttentionMsg:
    def __init__(self, content):
        self.content = content


class NextStepsMsg:
    def __init__(self, content):
        self.content = content


class FatalError(Exception):
    def __init__(self, message):
        super().__init__(message)