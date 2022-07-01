import os


class FileManager:
    __dirs__ = ["logs"]

    __files__ = {"input": "input.txt", "output": "output.txt", "log_translator": "logs/translator.log",
                 "log_syntax": "logs/syntax.log", "log_lexical": "logs/lexical.log"}

    def __checkpaths__(self):
        for dir in self.__dirs__:
            if not os.path.exists(dir):
                os.makedirs(dir)
        for file in self.__files__.values():
            if not os.path.exists(file):
                with open(file, 'w') as f_io:
                    f_io.close()

    def __clearlogs__(self):
        for log_file_key in filter(lambda x: "log_" in x, self.__files__.keys()):
            with open(self.__files__[log_file_key], "w") as f_io:
                f_io.write("")
                f_io.close()

    def input(self) -> str:
        """
        Function returns data from input file
        :return: str
        """
        input_data = ""
        with open(self.__files__['input'], 'r') as f_io:
            input_data = f_io.read()
            f_io.close()
        return input_data

    def output(self, data: str):
        """
        Function saves data to output file
        :return:
        """
        with open(self.__files__['output'], 'w') as f_io:
            f_io.write(data)
            f_io.close()

    def write_log(self, blockname: str, log_message: str):
        """
        Function writes a log message from block to his log file
        :param blockname: str
        :param log_message: str
        :return:
        """
        if f"log_{blockname.rstrip('.py')}" not in self.__files__.keys():
            print(f"Not found log file for {blockname}.")
            return
        log_file = self.__files__[f"log_{blockname.rstrip('.py')}"]

        with open(log_file, 'a') as f_io:
            f_io.write(log_message + "\n")
            f_io.close()

    def __init__(self):
        self.__checkpaths__()
        self.__clearlogs__()
