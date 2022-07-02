from lexical import *
import logging as logger


class SyntaxBlockError(Exception):
    pass


class SyntaxStatus(enum.Enum):
    start = 0
    service_name_const = 1
    space = 2
    identifier = 3
    equal = 4
    value = 5
    semicolon = 6
    error = 7


class Syntax:
    def __init__(self):
        pass

    def __transition__(self, __status: SyntaxStatus, __name: str, __wc: WordClass):

        status = __status

        match __wc:
            case WordClass.identifier:
                if __status == SyntaxStatus.space:
                    status = SyntaxStatus.identifier
                else:
                    status = SyntaxStatus.error
            case WordClass.number:
                if __status == SyntaxStatus.equal:
                    status = SyntaxStatus.value
                else:
                    status = SyntaxStatus.error
            case WordClass.hex_number:
                if __status == SyntaxStatus.equal:
                    status = SyntaxStatus.value
                else:
                    status = SyntaxStatus.error
            case WordClass.equal:
                if __status == SyntaxStatus.identifier:
                    status = SyntaxStatus.equal
                else:
                    status = SyntaxStatus.error
            case WordClass.semicolon:
                if __status == SyntaxStatus.value:
                    status = SyntaxStatus.semicolon
                else:
                    status = SyntaxStatus.error
            case WordClass.space:
                if __status == SyntaxStatus.service_name_const:
                    status = SyntaxStatus.space
                elif __status == SyntaxStatus.space:
                    status = SyntaxStatus.space
                else:
                    status = SyntaxStatus.error
            case WordClass.service_name:
                if __status == SyntaxStatus.start and __name.lower() == "const":
                    status = SyntaxStatus.service_name_const
                else:
                    status = SyntaxStatus.error

        return status

    def syntax_analyze(self, data: typing.List[typing.Tuple[str, WordClass]]) -> str:
        """
        Function analyzes a chain on syntactic match with example "CONST <identifier>=<value>;"
        Result: ACCEPT or REJECT or throws an SyntaxBlockError
        :param data: A list of tuple str and WordClass
        :return: str
        """
        fullchain = "".join([i[0] for i in data])
        status = SyntaxStatus.start

        for i in range(len(data)):
            name = data[i][0]
            wc = data[i][1]

            status = self.__transition__(status, name, wc)

            if status == SyntaxStatus.error:
                logger.log(f"Unexpected word \"{name}\"({wc}) in \"{fullchain}\"", logger.LogStatus.ERROR)
                raise SyntaxBlockError(f"Unexpected word \"{name}\"({wc}) in \"{fullchain}\"")

            logger.log(f"Word \"{name}\"({wc}) accepted.", logger.LogStatus.INFO)

        if status != SyntaxStatus.semicolon:
            logger.log(f"Excepted ';' in \"{fullchain}\"", logger.LogStatus.ERROR)
            raise SyntaxBlockError(f"Excepted ';' in \"{fullchain}\"")
        return "ACCEPT"


if __name__ == "__main__":
    lex = Lexical()
    trans = Translator()
    syntax = Syntax()
    lexems = trans.translate("var five=5;")
    lexems2 = lex.lexical_analyze(lexems)
    print(lexems2)
    result = syntax.syntax_analyze(lexems2)

    print(result)
