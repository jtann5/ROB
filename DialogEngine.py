
class UserRule:
    def __init__(self):
        self.subrules = {}


class ProposalRule:
    def __init__(self):
        self.subrules = {}


class DialogEngine:
    def __init__(self):
        self.DialogFile = None
        self.src_code = None

        self.line = 0
        self.lineOffset = 0
        variableMap = {}



    def setFile(self, file):
        self.DialogFile = file
    def openFile(self):
        file = open(self.DialogFile)
        self.src_code = file.read()

    def match(self, input):
        pass

    def print(self):
        # self.src_code[0..] is the character at the index
        print(self.src_code)


if __name__ == "__main__":
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()
    d.print()