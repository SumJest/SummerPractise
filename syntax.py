import logger
import enum
import typing

from lexical import Lexical, WordClass
from translator import SymbolClass, Translator
from utils.exceptions import SyntaxBlockError
from utils.objects import WordClass, SyntaxStatus, Lexeme


class Syntax:
    safe_mode: bool
    logging: bool

    def __init__(self, safe_mode: bool = False, logging: bool = True):
        self.safe_mode = safe_mode
        self.logging = logging

    def _transition(self, status: SyntaxStatus, lexeme: Lexeme):

        status = status

        match lexeme.content_type:
            case WordClass.identifier:
                if status == SyntaxStatus.service_name_const:
                    status = SyntaxStatus.identifier
                else:
                    status = SyntaxStatus.error
            case WordClass.number:
                if status == SyntaxStatus.equal or status == SyntaxStatus.sign:
                    status = SyntaxStatus.value
                else:
                    status = SyntaxStatus.error
            case WordClass.hex_number:
                if status == SyntaxStatus.equal:
                    status = SyntaxStatus.value
                else:
                    status = SyntaxStatus.error
            case WordClass.sign:
                if status == SyntaxStatus.equal:
                    status = SyntaxStatus.sign
                else:
                    status = SyntaxStatus.error
            case WordClass.equal:
                if status == SyntaxStatus.identifier:
                    status = SyntaxStatus.equal
                else:
                    status = SyntaxStatus.error
            case WordClass.semicolon:
                if status == SyntaxStatus.value:
                    status = SyntaxStatus.semicolon
                else:
                    status = SyntaxStatus.error
            case WordClass.space:
                # if status == SyntaxStatus.service_name_const:
                #     status = SyntaxStatus.space
                # elif status == SyntaxStatus.space:
                #     status = SyntaxStatus.space
                # else:
                #     status = SyntaxStatus.error
                pass
            case WordClass.const_name:
                status = SyntaxStatus.service_name_const
            case _:
                status = SyntaxStatus.error

        return status

    def syntax_analyze(self, data: typing.List[Lexeme]) -> str:
        """
        Function analyzes a chain on syntactic match with example "CONST <identifier>=<value>;"
        Result: ACCEPT or REJECT or throws an SyntaxBlockError if safe-mode off.
        :param data: A list of tuple str and WordClass
        :return: str
        """
        fullchain = "".join([i.content for i in data])
        status = SyntaxStatus.start

        for i in range(len(data)):
            lexeme = data[i]

            status = self._transition(status, lexeme)

            if status == SyntaxStatus.error:
                if self.logging:
                    logger.log(f"Unexpected word {lexeme} in \"{fullchain}\"", logger.LogStatus.ERROR)
                if self.safe_mode:
                    return "REJECT"
                else:
                    raise SyntaxBlockError(f"Unexpected word {lexeme} in \"{fullchain}\"")

            if self.logging:
                logger.log(f"Word {lexeme} accepted.", logger.LogStatus.INFO)

        if status != SyntaxStatus.semicolon:
            if self.logging:
                logger.log(f"Excepted ';' in \"{fullchain}\"", logger.LogStatus.ERROR)
            if self.safe_mode:
                return "REJECT"
            else:
                raise SyntaxBlockError(f"Excepted ';' in \"{fullchain}\"")
        return "ACCEPT"


if __name__ == "__main__":
    lex = Lexical()
    trans = Translator()
    syntax = Syntax()
    lexems = trans.translate("const five=      $ 1;")
    lexems2 = lex.lexical_analyze(lexems)
    print(lexems2)
    result = syntax.syntax_analyze(lexems2)

    print(result)
