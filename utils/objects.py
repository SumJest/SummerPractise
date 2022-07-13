import enum


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
    sign = 7
    other = 8

    def __repr__(self):
        return f"{self.name}"


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


class SyntaxStatus(enum.Enum):
    start = 0
    service_name_const = 1
    space = 2
    identifier = 3
    equal = 4
    value = 5
    semicolon = 6
    sign = 7
    error = 8


class Lexeme:
    content: str
    content_type: SymbolClass | WordClass

    def __init__(self, content: str, content_type: SymbolClass | WordClass):
        self.content = content
        self.content_type = content_type

    def __repr__(self):
        return f"(\"{self.content}\",{self.content_type})"
