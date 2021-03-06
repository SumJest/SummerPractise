import os


class FileManager:
    __dirs = ["logs"]

    __files = {"input": "input.txt", "output": "output.txt", "log_translator": "logs/translator.log",
               "log_syntax": "logs/syntax.log", "log_lexical": "logs/lexical.log"}

    def _checkpaths(self):
        for dir in self.__dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)
        for file in self.__files.values():
            if not os.path.exists(file):
                with open(file, 'w') as f_io:
                    f_io.close()

    def _clearlogs(self):
        for log_file_key in filter(lambda x: "log_" in x, self.__files.keys()):
            with open(self.__files[log_file_key], "w") as f_io:
                f_io.write("")
                f_io.close()

    def input(self) -> str:
        """
        Function returns data from input file
        :return: str
        """
        with open(self.__files['input'], 'r') as f_io:
            input_data = f_io.read()
            f_io.close()
        return input_data

    def output(self, data: str):
        """
        Function saves data to output file
        :return:
        """
        with open(self.__files['output'], 'w') as f_io:
            f_io.write(data)
            f_io.close()

    def write_log(self, blockname: str, log_message: str):
        """
        Function writes a log message from block to his log file
        :param blockname: str
        :param log_message: str
        :return:
        """
        if f"log_{blockname}" not in self.__files.keys():
            print(f"Not found log file for {blockname}.")
            return
        log_file = self.__files[f"log_{blockname.rstrip('.py')}"]

        with open(log_file, 'a') as f_io:
            f_io.write(log_message + "\n")
            f_io.close()

    def __init__(self):
        self._checkpaths()
        self._clearlogs()
