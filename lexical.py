import enum
import typing
import logger
from translator import Translator, SymbolClass
from utils.exceptions import LexicalBlockError
from utils.objects import SymbolClass, WordClass, WordStatus


class Lexical:
    safe_mode: bool
    logging: bool
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

    def __init__(self, safe_mode: bool = False, logging: bool = True):
        self.safe_mode = safe_mode
        self.logging = logging
        self.words = []

    def _collapse(self):

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

    def _transition(self, __status: WordStatus, __sc: SymbolClass, __name: str):

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

    def _keywordanalyze(self):

        for i in range(len(self.words)):
            if self.words[i][0].lower() in self.keywords_list:
                self.words[i] = (self.words[i][0], WordClass.service_name)
                if self.logging:
                    logger.log(f"Word \"{self.words[i][0]}\" recognized as {self.words[i][1]}", logger.LogStatus.INFO)

    def lexical_analyze(self, data: typing.List[typing.Tuple[str, SymbolClass]]) -> \
            typing.List[typing.Tuple[str, WordClass]] | None:
        """
        Function finds suitable words of WordClass in the chain
        :param data: list(str,SymbolClass)
        :return: list(str, WordClass) or None if safe-mode
        """
        fullchain = "".join([i[0] for i in data])
        self.words = []
        status = WordStatus.idle
        for i in range(len(data)):
            letter = data[i]

            status = self._transition(status, letter[1], letter[0])

            if status == WordStatus.error:
                if self.logging:
                    logger.log(f"Unexpected symbol \"{letter[0]}\" by index {i} in \"{fullchain}\"",
                               logger.LogStatus.ERROR)
                if self.safe_mode:
                    return None
                else:
                    raise LexicalBlockError(f"Unexpected symbol \"{letter[0]}\" by index {i} in \"{fullchain}\"")
            if status == WordStatus.hex_number_letter or status == WordStatus.hex_number_digit:
                wc = WordClass.hex_number
            elif status == WordStatus.idle:
                wc = getattr(WordClass, letter[1].name)
            else:
                wc = getattr(WordClass, status.name)

            self.words.append((letter[0], wc))
            self._collapse()
            last_word = self.words[len(self.words) - 1]
            if self.logging:
                logger.log(f"Word \"{last_word[0]}\" recognized as {last_word[1]}", logger.LogStatus.INFO)

        self._keywordanalyze()
        return self.words


if __name__ == "__main__":
    lex = Lexical()
    trans = Translator()
    lex_trans = trans.translate("const uno=$1h;")
    print(lex_trans)
    lexems = lex.lexical_analyze(lex_trans)
    print(lexems)
