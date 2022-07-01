import enum
import typing
from blocks import logging as logger
from blocks.translator import *


class LexicalError(Exception):
    pass


class WordStatus(enum.Enum):
    idle = 0
    identifier = 1
    number = 2
    hex_number_letter = 3
    hex_number_digit = 4
    error = 5

    def __repr__(self):
        return f"{self.name}"


class WordClass(enum.Enum):
    identifier = 0
    number = 1
    hex_number = 2
    equal = 3
    semicolon = 4
    space = 5
    service_name = 6
    other = 7

    def __repr__(self):
        return f"{self.name}"


class Lexical:
    words: typing.List[typing.Tuple[str, WordClass]]

    keywords_list = ["and", "array", "asm", "begin", "break", "case", "const", "constructor", "continue", "destructor",
                     "div",
                     "do", "downto", "else", "end", "false", "file", "for", "function", "goto", "if", "implementation",
                     "in",
                     "inline", "interface", "label", "mod", "nil", "not", "object", "of", "on", "operator", "or",
                     "packed",
                     "procedure", "program", "record", "repeat", "set", "shl", "shr", "string", "then", "to", "true",
                     "type",
                     "unit", "until", "uses", "var", "while", "with", "xor"]

    def __init__(self):
        self.words = []

    def __collapse__(self):

        if self.words[len(self.words) - 1][1] != WordClass.number and \
                self.words[len(self.words) - 1][1] != WordClass.identifier and \
                self.words[len(self.words) - 1][1] != WordClass.hex_number:
            return

        word = self.words.pop()
        buffer = word[0]
        wc = word[1]
        while len(self.words) > 0 and self.words[len(self.words) - 1][1] == wc:
            word = self.words.pop()
            buffer = word[0] + buffer
        self.words.append((buffer, wc))

    def __transition__(self, __status: WordStatus, __sc: SymbolClass, __name: str):

        status = __status
        match __sc:
            case SymbolClass.letter:
                match __status:
                    case WordStatus.idle:
                        status = WordStatus.identifier
                    case WordStatus.identifier:
                        status = WordStatus.identifier
                    case WordStatus.hex_number_letter:
                        if ord('A') <= ord(__name) <= ord('F') or ord('a') <= ord(__name) <= ord('f'):
                            status = WordStatus.hex_number_letter
                        else:
                            status = WordStatus.error
                    case WordStatus.hex_number_digit:
                        if ord('A') <= ord(__name) <= ord('F') or ord('a') <= ord(__name) <= ord('f'):
                            status = WordStatus.hex_number_letter
                        else:
                            status = WordStatus.error
                    case _:
                        status = WordStatus.error
            case SymbolClass.digit:
                match __status:
                    case WordStatus.idle:
                        status = WordStatus.number
                    case WordStatus.identifier:
                        status = WordStatus.identifier
                    case WordStatus.number:
                        status = WordStatus.number
                    case WordStatus.hex_number_letter:
                        status = WordStatus.hex_number_digit
                    case WordStatus.hex_number_digit:
                        status = WordStatus.hex_number_digit
                    case _:
                        status = WordStatus.error
            case SymbolClass.sign:
                match __status:
                    case WordStatus.idle:
                        status = WordStatus.number
                    case _:
                        status = WordStatus.error
            case SymbolClass.equal:
                match __status:
                    case WordStatus.hex_number_letter:
                        status = WordStatus.error
                    case WordStatus.error:
                        status = WordStatus.error
                    case _:
                        status = WordStatus.idle
            case SymbolClass.dollar:
                match __status:
                    case WordStatus.idle:
                        status = WordStatus.hex_number_digit
                    case _:
                        status = WordStatus.error
            case SymbolClass.semicolon:
                match __status:
                    case WordStatus.hex_number_letter:
                        status = WordStatus.error
                    case WordStatus.error:
                        status = WordStatus.error
                    case _:
                        status = WordStatus.idle
            case SymbolClass.space:
                match __status:
                    case WordStatus.hex_number_letter:
                        status = WordStatus.error
                    case WordStatus.error:
                        status = WordStatus.error
                    case _:
                        status = WordStatus.idle
        return status

    def __keywordanalyze__(self):

        for i in range(len(self.words)):
            if self.words[i][0].lower() in self.keywords_list:
                self.words[i] = (self.words[i][0], WordClass.service_name)
                logger.log(f"Word \"{self.words[i][0]}\" recognized as {self.words[i][1]}", logger.LogStatus.INFO)

    def lexical_analyze(self, data: typing.List[typing.Tuple[str, SymbolClass]]) -> \
            typing.List[typing.Tuple[str, WordClass]]:
        """
        Function finds suitable words of WordClass in the chain
        :param data: list(str,SymbolClass)
        :return: list(str, WordClass)
        """
        fullchain = "".join([i[0] for i in data])
        self.words = []
        status = WordStatus.idle
        for i in range(len(data)):
            letter = data[i]

            status = self.__transition__(status, letter[1], letter[0])

            if status == WordStatus.error:
                logger.log(f"Unexpected symbol \"{letter[0]}\" by index {i} in \"{fullchain}\"", logger.LogStatus.ERROR)
                raise LexicalError(f"Unexpected symbol \"{letter[0]}\" by index {i} in \"{fullchain}\"")
            if status == WordStatus.hex_number_letter or status == WordStatus.hex_number_digit:
                wc = WordClass.hex_number
            elif status == WordStatus.idle:
                wc = getattr(WordClass, letter[1].name)
            else:
                wc = getattr(WordClass, status.name)

            self.words.append((letter[0], wc))
            self.__collapse__()
            last_word = self.words[len(self.words) - 1]
            logger.log(f"Word \"{last_word[0]}\" recognized as {last_word[1]}", logger.LogStatus.INFO)

        self.__keywordanalyze__()
        return self.words


if __name__ == "__main__":
    lex = Lexical()
    trans = Translator()
    lexems = trans.translate("const a=$1;")
    for lex in lex.lexical_analyze(lexems):
        print(lex)
