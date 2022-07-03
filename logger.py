import datetime
import enum
import inspect
from filemanager import FileManager

fm = FileManager()


class LogStatus(enum.Enum):
    INFO = 0
    WARN = 1
    ERROR = 2


def get_block_name(frame) -> str:
    """
    Function gets filename from frame which called function.
    :param frame: FramType
    :return: str
    """
    return frame.f_code.co_filename.split('\\').pop()


def getNowTime() -> str:
    """
    Function format current time
    :return: str
    """
    return datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")


def log(msg: str, status: LogStatus):
    """
    Function build a log message and send to write it in log file
    :param msg: str
    :param status: LogStatus
    :return:
    """
    blockname = get_block_name(inspect.currentframe().f_back)
    time = getNowTime()
    log_message = f"[{status.name}] [{time}] {blockname}: {msg}"
    fm.write_log(blockname, log_message)
    print(log_message)
