import typing

import logger

from utils.exceptions import TranslatorBlockError
from utils.objects import SymbolClass, Lexeme


class Translator:
    safe_mode: bool
    logging: bool

    def __init__(self, safe_mode: bool = False, logging: bool = True):
        self.safe_mode = safe_mode
        self.logging = logging

    def _recognize(self, letter: str) -> SymbolClass | None:
        if len(letter) != 1:
            return None
        letter_code = ord(letter)
        if ord('a') <= letter_code <= ord('z') or ord('A') <= letter_code <= ord("Z"):
            return SymbolClass.letter
        elif ord('0') <= letter_code <= ord('9'):
            return SymbolClass.digit

        match letter:
            case "+":
                return SymbolClass.sign
            case "-":
                return SymbolClass.sign
            case "=":
                return SymbolClass.equal
            case "$":
                return SymbolClass.dollar
            case ";":
                return SymbolClass.semicolon
            case " ":
                return SymbolClass.space
            case _:
                return SymbolClass.other

    def translate(self, data: str) -> typing.List[Lexeme] | None:
        """
        Function translates string line data and returns list of tuples that contain letter and class of letter.
        :param data: str
        :return: list(str,SymbolClass), None if safe-mode.
        """
        data = data.rstrip("\n")
        result = []
        for i in range(len(data)):
            sc = self._recognize(data[i])
            if sc == SymbolClass.other:
                if self.logging:
                    logger.log(f"Unexpected symbol \"{data[i]}\" by index {i} in \"{data}\"", logger.LogStatus.ERROR)
                if self.safe_mode:
                    return None
                else:
                    raise TranslatorBlockError(f"Unexpected symbol \"{data[i]}\" by index {i} in \"{data}\"")
            if self.logging:
                logger.log(f"Letter \"{data[i]}\" recognized as {sc}", logger.LogStatus.INFO)
            result.append(Lexeme(data[i], sc))
        return result


if __name__ == "__main__":
    translator = Translator()
    print(translator.translate("const ac=+1;"))
