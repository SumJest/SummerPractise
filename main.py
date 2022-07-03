import traceback

from filemanager import FileManager
from translator import Translator
from lexical import Lexical
from syntax import Syntax
from utils.exceptions import RecognizerError

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
    except RecognizerError as ex:
        print(ex.args[0])
        return "REJECT"


def main():
    input_data = fm.input()
    result = check(input_data)
    fm.output(result)


if __name__ == "__main__":
    main()
