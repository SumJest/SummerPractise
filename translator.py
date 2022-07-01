import enum
import typing


class TranslatorError(Exception):
    pass


class SymbolClass(enum.Enum):
    letter = 0
    digit = 1
    sign = 2
    equal = 3
    dollar = 4
    semicolon = 5
    space = 6
    other = 7

def __repr__(self):
    return f"{self.name}"


class Translator:

    def __init__(self):
        pass

    def __recognize__(self, letter: str) -> SymbolClass | None:
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

    def translate(self, data: str) -> typing.List[typing.Tuple[str, SymbolClass]]:
        """
        Function translates string line data and returns list of tuples that contain letter and class of letter
        :param data: str
        :return: list(str,SymbolClass)
        """
        data = data.rstrip("\n")
        result = []
        for i in range(len(data)):
            sc = self.__recognize__(data[i])
            if sc == SymbolClass.other:
                raise TranslatorError(f"Unexpected symbol \"{data[i]}\" by index {i} in \"{data}\"")
            result.append((data[i], sc))
        return result


if __name__ == "__main__":
    translator = Translator()
    print(translator.translate("const HEX=$10A1;"))
