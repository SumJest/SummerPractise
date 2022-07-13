import enum
import typing
import logger
from translator import Translator, SymbolClass
from utils.exceptions import LexicalBlockError
from utils.objects import SymbolClass, WordClass, WordStatus, Lexeme


class Lexical:
    safe_mode: bool
    logging: bool
    words: typing.List[Lexeme]

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

        if self.words[-1].content_type != WordClass.number and \
                self.words[-1].content_type != WordClass.identifier and \
                self.words[-1].content_type != WordClass.hex_number:
            return

        word = self.words.pop()
        buffer = word.content
        wc = word.content_type
        while len(self.words) > 0 and self.words[-1].content_type == wc:
            word = self.words.pop()
            buffer = word.content + buffer
        self.words.append(Lexeme(buffer, wc))

    def _transition(self, status: WordStatus, lexeme: Lexeme):

        status = status
        match lexeme.content_type:
            case SymbolClass.letter:
                match status:
                    case WordStatus.idle:
                        status = WordStatus.identifier
                    case WordStatus.identifier:
                        status = WordStatus.identifier
                    case _:
                        status = WordStatus.error
            case SymbolClass.hex_letter:
                match status:
                    case WordStatus.idle:
                        status = WordStatus.identifier
                    case WordStatus.identifier:
                        status = WordStatus.identifier
                    case WordStatus.hex_number_letter:
                        status = WordStatus.hex_number_letter
                    case WordStatus.hex_number_digit:
                        status = WordStatus.hex_number_letter
                    case _:
                        status = WordStatus.error
            case SymbolClass.digit:
                match status:
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
                match status:
                    case WordStatus.idle:
                        status = WordStatus.idle
                    case _:
                        status = WordStatus.error
            case SymbolClass.equal:
                match status:
                    case WordStatus.hex_number_letter:
                        status = WordStatus.error
                    case WordStatus.error:
                        status = WordStatus.error
                    case _:
                        status = WordStatus.idle
            case SymbolClass.dollar:
                match status:
                    case WordStatus.idle:
                        status = WordStatus.hex_number_letter
                    case _:
                        status = WordStatus.error
            case SymbolClass.semicolon:
                match status:
                    case WordStatus.hex_number_letter:
                        status = WordStatus.error
                    case WordStatus.error:
                        status = WordStatus.error
                    case _:
                        status = WordStatus.idle
            case SymbolClass.space:
                match status:
                    case WordStatus.hex_number_letter:
                        status = WordStatus.error
                    case WordStatus.error:
                        status = WordStatus.error
                    case _:
                        status = WordStatus.idle
        return status

    def _keywordanalyze(self):

        for i in range(len(self.words)):
            if self.words[i].content.lower() in self.keywords_list:
                if self.words[i].content.lower() == 'const':
                    self.words[i].content_type = WordClass.const_name
                else:
                    self.words[i].content_type = WordClass.service_name
                if self.logging:
                    logger.log(f"Word \"{self.words[i].content}\" recognized as {self.words[i].content_type}",
                               logger.LogStatus.INFO)

    def lexical_analyze(self, data: typing.List[Lexeme]) -> \
            typing.List[Lexeme] | None:
        """
        Function finds suitable words of WordClass in the chain
        :param data: list(str,SymbolClass)
        :return: list(str, WordClass) or None if safe-mode
        """
        fullchain = "".join([i.content for i in data])

        self.words = []
        status = WordStatus.idle

        for i in range(len(data)):
            lex = data[i]

            status = self._transition(status, lex)

            if status == WordStatus.error:
                if self.logging:
                    logger.log(f"Unexpected symbol \"{lex.content}\" by index {i} in \"{fullchain}\"",
                               logger.LogStatus.ERROR)
                if self.safe_mode:
                    return None
                else:
                    raise LexicalBlockError(f"Unexpected symbol \"{lex.content}\" by index {i} in \"{fullchain}\"")
            if status == WordStatus.hex_number_letter or status == WordStatus.hex_number_digit:
                wc = WordClass.hex_number
            elif status == WordStatus.idle:
                wc = getattr(WordClass, lex.content_type.name)
            else:
                wc = getattr(WordClass, status.name)

            self.words.append(Lexeme(lex.content, wc))
            self._collapse()
            last_word = self.words[-1]
            if self.logging:
                logger.log(f"Word \"{last_word.content}\" recognized as {last_word.content_type}",
                           logger.LogStatus.INFO)

        self._keywordanalyze()
        return self.words


if __name__ == "__main__":
    lex = Lexical()
    trans = Translator()
    lex_trans = trans.translate("const a = - 4  4;")
    print(lex_trans)
    lexems = lex.lexical_analyze(lex_trans)
    print(lexems)
