from filemanager import FileManager
from syntax import *

fm = FileManager()
translatorblock = Translator()
lexicalblock = Lexical()
syntaxblock = Syntax()


def check(expression: str) -> str:
    try:
        translator_result = translatorblock.translate(expression)
        lexical_result = lexicalblock.lexical_analyze(translator_result)
        syntax_result = syntaxblock.syntax_analyze(lexical_result)
        return syntax_result
    except Exception as ex:
        print(ex.args[0])
        return "REJECT"


def main():
    inputdata = fm.input()
    result = check(inputdata)
    fm.output(result)


if __name__ == "__main__":
    main()
