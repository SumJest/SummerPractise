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
        syntax_result = syntaxblock.syntax_analyze(lexical_result, full_chain=expression)
        return syntax_result
    except RecognizerError:
        return "REJECT"


def main():
    # input_data = input()
    # while input_data:
    input_data = fm.input()
    print(input_data)
    result = check(input_data)
        # print(result)
        # input_data = input()
    fm.output(result)


if __name__ == "__main__":
    main()
