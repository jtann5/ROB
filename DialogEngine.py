
class UserRule:
    def __init__(self, input):
        self.id = input
        self.subrules = {}
        self.input = None
        self.output = None

    def setInput(self, input):
        self.input = input

    def setOutput(self, output):
        self.output = output

class ProposalRule:
    def __init__(self):
        self.subrules = {}


class DialogEngine:
    def __init__(self):
        self.DialogFile = None
        self.src_code = None

        self.line = 0
        self.lineOffset = 0
        self.char = ''
        self.variableMap = {}
        self.rootUserRules = {}
        self.rootProposalRules = {}


    def setFile(self, file):
        self.DialogFile = file
    def openFile(self):
        file = open(self.DialogFile)
        self.src_code = file.read()
        self.parseFile()

    def updateChar(self):
        self.char = self.src_code[self.lineOffset]

    def parseFile(self):
        try:
            while self.lineOffset < len(self.src_code):
                # consumes comments and are ignored
                if self.match("#"):
                    while not self.match("\n"):
                        self.consume()
                    self.consume()
                elif self.match("~"):
                    while not self.match("\n"):
                        self.consume()
                    self.consume()
                elif self.src_code[self.lineOffset].isalnum():
                    print("MAde it here")
                    startIndex = self.lineOffset
                    self.require(':')
                    endIndex = self.lineOffset
                    rule = UserRule(self.src_code[startIndex:endIndex])
                    self.require('(')
                    inputstart = self.lineOffset+1
                    self.require(')')
                    inputend = self.lineOffset-1
                    rule.setInput(self.src_code[inputstart:inputend])
                    self.require(':')
                    responsestart = self.lineOffset+1
                    self.require('\n')
                    responseend = self.lineOffset
                    rule.setOutput(self.src_code[responsestart:responseend])
                    self.rootUserRules[rule.input] = rule
                    print(rule.id)
                    self.consume()


        except EOFError as e:
            print(e)

    def getResponse(self):
        pass

    def match(self, input):
        if self.src_code[self.lineOffset] == input:
            return True
        return False

    def matchandconsume(self, input):
        if self.match(input):
            self.consume()
            return True
        return False

    def consume(self):
        self.lineOffset += 1
        self.updateChar()

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
                if (self.src_code[self.lineOffset] == input) or (self.src_code[self.lineOffset] == '\n'):
                    break
                else:
                    self.consume()
        except SyntaxError as e:
            print(e)

if __name__ == "__main__":
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()
    print(d.rootUserRules)
    # d.print()