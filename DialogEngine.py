import re
import random

class UserRule:
    def __init__(self, input):
        self.id = input
        self.subrules = {}
        self.input = None
        self.output = None
        self.parent = None

    def setInput(self, input):
        self.input = input

    def setOutput(self, output):
        self.output = output

class ProposalRule:
    def __init__(self, input):
        self.id = input
        self.subrules = {}


class DialogEngine:
    def __init__(self):
        self.DialogFile = None
        self.src_code = None
        self.treelevel = None

        self.line = 0
        self.lineOffset = 0
        self.char = ''
        self.variableMap = {}
        self.predefinedvarMap = {}
        self.rootUserRules = {}
        self.rootProposalRules = {}


    def setFile(self, file):
        self.DialogFile = file
    def openFile(self):
        file = open(self.DialogFile)
        self.src_code = file.read()
        self.parseFile()

    def updateChar(self):
        if self.lineOffset < len(self.src_code):
            self.char = self.src_code[self.lineOffset]

    def parseFile(self):
        parentrule = None
        try:
            while self.lineOffset < len(self.src_code):
                # consumes comments and are ignored
                if self.match("#"):
                    while not self.match('\n'):
                        self.consume()
                    self.consume()
                elif self.match("~"):
                    varNameStart = self.lineOffset
                    self.require(':')
                    varNameEnd = self.lineOffset
                    self.consume()
                    self.consumewhitespace()
                    answerList = []
                    while not self.match('\n'):
                        if self.matchandconsume('"'):
                            varStart = self.lineOffset
                            self.require('"')
                            varEnd = self.lineOffset
                            var = self.src_code[varStart:varEnd]
                            self.consume()
                            answerList.append(var)
                            self.consume()
                        elif self.match('['):
                            self.consume()
                            while not self.match('\n'):
                                if self.matchandconsume('"'):
                                    varStart = self.lineOffset
                                    self.require('"')
                                    varEnd = self.lineOffset
                                    var = self.src_code[varStart:varEnd]
                                    self.consume()
                                    answerList.append(var)
                                    self.consume()
                                else:
                                    start = self.lineOffset
                                    self.require([' ', ']'])
                                    end = self.lineOffset
                                    var = self.src_code[start:end]
                                    answerList.append(var)
                                    if end < len(self.src_code):
                                        if self.src_code[end] != '\n':
                                            self.consume()
                        elif self.match(']'):
                            self.consume()
                        elif self.lineOffset >= (len(self.src_code) - 1):
                            break
                        else:
                            start = self.lineOffset
                            while not self.match('\n') and self.lineOffset < len(self.src_code):
                                self.consume()
                            end = self.lineOffset
                            var = self.src_code[start:end]
                            answerList.append(var)
                    self.predefinedvarMap[self.src_code[varNameStart:varNameEnd]] = answerList
                    self.consume()
                elif self.src_code[self.lineOffset].isalnum():
                    startIndex = self.lineOffset
                    self.require(':')
                    endIndex = self.lineOffset
                    rule = UserRule(self.src_code[startIndex:endIndex])
                    self.require('(')
                    inputstart = self.lineOffset+1
                    self.require(')')
                    inputend = self.lineOffset
                    rule.setInput(self.src_code[inputstart:inputend])
                    self.require(':')
                    self.consume()
                    responseList = []
                    self.consumewhitespace()
                    while not self.match('\n'):
                        if self.matchandconsume('"'):
                            varStart = self.lineOffset
                            self.require('"')
                            varEnd = self.lineOffset
                            var = self.src_code[varStart:varEnd]
                            self.consume()
                            responseList.append(var)
                            self.consume()
                        elif self.match('['):
                            self.consume()
                            while not self.match('\n'):
                                if self.matchandconsume('"'):
                                    varStart = self.lineOffset
                                    self.require('"')
                                    varEnd = self.lineOffset
                                    var = self.src_code[varStart:varEnd]
                                    self.consume()
                                    responseList.append(var)
                                    self.consume()
                                else:
                                    start = self.lineOffset
                                    self.require([' ', ']'])
                                    end = self.lineOffset
                                    var = self.src_code[start:end]
                                    responseList.append(var)
                                    if end < len(self.src_code):
                                        if self.src_code[end] != '\n':
                                            self.consume()
                        elif self.match(']'):
                            self.consume()
                        elif self.lineOffset >= (len(self.src_code) - 1):
                            break
                        else:
                            start = self.lineOffset
                            while not self.match('\n') and self.lineOffset < len(self.src_code):
                                self.consume()
                            end = self.lineOffset
                            var = self.src_code[start:end]
                            responseList.append(var)

                    if self.lineOffset < len(self.src_code):
                        if self.src_code[self.lineOffset] != '\n':
                            self.consume()

                    rule.setOutput(responseList)

                    if parentrule is not None:
                        parentscope = self.extract_scope(parentrule.id)
                        childscope = self.extract_scope(rule.id)
                        if childscope-1 == parentscope:
                            rule.parent = parentrule
                            parentrule.subrules[rule.input] = rule
                            parentrule = rule
                        elif childscope == 0:
                            self.rootUserRules[rule.input] = rule
                            parentrule = rule
                        else:
                            parentrule = parentrule.parent
                            parentrule.subrules[rule.input] = rule
                            parentrule = rule
                    else:
                        self.rootUserRules[rule.input] = rule
                        parentrule = rule

                    self.consume()

                self.consumewhitespace()

        except EOFError as e:
            print(e)


    def getResponse(self):
        pass

    def match(self, input):
        if (self.lineOffset < len(self.src_code)) and (self.src_code[self.lineOffset] == input):
            return True
        return False

    def extract_scope(self, identifier):
        match = re.match(r'^u(\d+)$', identifier)
        if match:
            return int(match.group(1))
        else:
            return 0

    def matchandconsume(self, input):
        if self.match(input):
            self.consume()
            return True
        return False

    def consume(self):
        self.lineOffset += 1
        self.updateChar()

    def consumewhitespace(self):
        while self.lineOffset < len(self.src_code):
            if self.src_code[self.lineOffset].isspace():
                self.consume()
            else:
                break

    def print(self):
        # self.src_code[0..] is the character at the index
        try:
            index = 0
            while index < len(self.src_code):
                index += 1
        except EOFError as e:
            print(e)

    def require(self, input):
        try:
            while self.lineOffset < len(self.src_code):
                if isinstance(input, list):
                    for item in input:
                        if (self.src_code[self.lineOffset] == item) or (self.src_code[self.lineOffset] == '\n'):
                            return
                    self.consume()
                else:
                    if (self.src_code[self.lineOffset] == input) or (self.src_code[self.lineOffset] == '\n'):
                        return
                    else:
                        self.consume()
        except SyntaxError as e:
            print(e)

    def analyze(self, input):
        testBool = True
        output = ""
        if input.__contains__("_"):
            input.replace("_", "\w+")
        if testBool:
            for option in self.predefinedvarMap:
                for item in self.predefinedvarMap[option]:
                    if input == item:
                        output += random.choice(self.rootUserRules[option].output)
                        self.treelevel = self.rootUserRules[option]
                        testBool = True
                        break
                    testBool = False
        if (self.treelevel is not None) and (testBool != True):
            if input in self.treelevel.subrules:
                rule_output = random.choice(self.treelevel.subrules[input].output)
                for var in self.variableMap:
                    if rule_output.__contains__(var):
                        rule_output = rule_output.replace(var, self.variableMap[var])
                self.treelevel = self.treelevel.subrules[input]
                if rule_output.startswith('~'):
                    for option in self.predefinedvarMap:
                        if rule_output == option:
                            output += random.choice(self.rootUserRules[option].output)
                            break
                else:
                    output += rule_output
                testBool = True
            else:
                temp = self.treelevel.parent
                while temp is not None:
                    if input == temp.input:
                        output += random.choice(temp.output)
                        testBool = True
                        self.treelevel = temp
                        break
                    else:
                        temp = temp.parent
        if (input in self.rootUserRules) and (testBool != True):
            rule_output = random.choice(self.rootUserRules[input].output)
            for var in self.variableMap:
                if rule_output.__contains__(var):
                    rule_output = rule_output.replace(var, self.variableMap[var])
            self.treelevel = self.rootUserRules[input]
            if rule_output.startswith('~'):
                for option in self.predefinedvarMap:
                    if input == option:
                        output += random.choice(self.rootUserRules[option].output)
                        break
            else:
                output += rule_output
            testBool = True

        if not testBool:
            for item in d.rootUserRules:
                name = item.replace("_", "(.*)")
                match = re.match(name, input)
                if match:
                    var_name = ""
                    outputval = random.choice(d.rootUserRules[item].output)
                    match2 = re.search(r'\$[a-zA-Z_][a-zA-Z0-9_]*', outputval)
                    if match2:
                        var_name = match2.group()
                        matched_value = match.group(1)
                        self.variableMap[var_name] = matched_value
                        #print(self.variableMap)
                        var = self.variableMap[var_name]
                        output += outputval.replace(var_name, var)
                        self.treelevel = d.rootUserRules[item]
                else:
                    rule_name = self.analyzeVarHelper(d.rootUserRules[item].subrules, input)
                    if rule_name is not None:
                        output += rule_name
            if output == "":
                output += "No rules found for that prompt"

        output += " "
        return output

    def analyzeVarHelper(self, value, input):
        for item in value:
            name = item.replace("_", "(.*)")
            match = re.match(name, input)
            if match:
                var_name = ""
                outputval = random.choice(value[item].output)
                match2 = re.search(r'\$[a-zA-Z_][a-zA-Z0-9_]*', outputval)
                if match2:
                    var_name = match2.group()
                    matched_value = match.group(1)
                    self.variableMap[var_name] = matched_value
                    # print(self.variableMap)
                    var = self.variableMap[var_name]
                    self.tree_level = value[item].subrules
                    return outputval.replace(var_name, var)
            else:
                rule_name = self.analyzeVarHelper(value[item].subrules, input)
                if rule_name is not None:
                    print(rule_name)
        return None


def printchild(list):
    for i in list.values:
        print(i)
        printchild(list[i].subrules)


def userrulehelper(list, indent):
    for item in list:
        temp_indent = indent*4
        str = " " * temp_indent
        print(str + item, list[item].subrules)
        userrulehelper(list[item].subrules, indent+1)

def printuserrules():
    for item in d.rootUserRules:
        print(item, d.rootUserRules[item].subrules)
        userrulehelper(d.rootUserRules[item].subrules, indent=1)

def outputvariables():
    for item in d.rootUserRules:
        print(item, d.rootUserRules[item].output)
        outputvariablehelper(d.rootUserRules[item].subrules, indent=1)

def outputvariablehelper(list, indent):
    for item in list:
        temp_indent = indent*4
        str = " " * temp_indent
        print(str + item, list[item].output)
        outputvariablehelper(list[item].subrules, indent+1)

if __name__ == "__main__":
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()
    #print(d.predefinedvarMap)
    #printuserrules()
    # outputvariables()

    #print(d.predefinedvarMap)
    #print(d.predefinedvarMap['~greetings'])

    x = "placeholder"
    while x != "bye":
        x = input("Human: ")
        if x == "bye":
            break
        output = d.analyze(x.strip())
        print("Robot: " + output)
