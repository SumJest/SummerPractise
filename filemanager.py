import os


class FileManager:
    __dirs__ = ["logs"]
    __files__ = ["input.txt", "output.txt", "logs/keywords.log", "logs/lexer.log", "logs/transliterator.log",
                 "logs/syntax.log", "logs/system.log"]
    __inputfile__ = "input.txt"
    __outputfile__ = "output.txt"

    def __checkpaths__(self):
        for dir in self.__dirs__:
            if not os.path.exists(dir):
                os.makedirs(dir)
        for file in self.__files__:
            if not os.path.exists(file):
                with open(file, 'w') as f_io:
                    f_io.close()

    def input(self) -> str:
        """
        Function returns data from input file
        :return: str
        """
        input_data = ""
        with open(self.__inputfile__, 'r') as f_io:
            input_data = f_io.read()
            f_io.close()
        return input_data

    def output(self, data: str):
        """
        Function saves data to output file
        :return:
        """
        with open(self.__outputfile__, 'w') as f_io:
            f_io.write(data)
            f_io.close()

    def __init__(self):
        self.__checkpaths__()
