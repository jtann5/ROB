
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
        try:
            index = 0
            while index < len(self.src_code):
                # consumes comments
                if self.match("#"):
                    while not self.match("\n"):
                        self.consume()

        except EOFError as e:
            print(e)

    def match(self, input):
        if self.src_code[self.lineOffset] == input:
            return True
        return False

    def matchandconsume(self, input):
        if self.match(input):
            self.lineOffset += 1
            return True
        return False

    def consume(self):
        self.lineOffset += 1

    def print(self):
        # self.src_code[0..] is the character at the index
        try:
            index = 0
            while index < len(self.src_code):
                print(self.src_code[index])
                index += 1
        except EOFError as e:
            print(e)


if __name__ == "__main__":
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()
    d.print()