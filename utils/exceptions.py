class RecognizerError(Exception):
    pass


class LexicalBlockError(RecognizerError):
    pass


class TranslatorBlockError(RecognizerError):
    pass


class SyntaxBlockError(RecognizerError):
    pass
