import traceback

from filemanager import FileManager
from lexical import *
from translator import *
from syntax import *

fm = FileManager()
translatorblock = Translator()
lexicalblock = Lexical()
syntaxblock = Syntax()


def main():
    try:
        inputdata = fm.input()
        translatorresult = translatorblock.translate(inputdata)
        lexicalresult = lexicalblock.lexical_analyze(translatorresult)
        syntaxresult = syntaxblock.syntax_analyze(lexicalresult)
        fm.output(syntaxresult)
    except Exception:
        print(traceback.format_exc())
        fm.output("REJECTED")


if __name__ == "__main__":
    main()
