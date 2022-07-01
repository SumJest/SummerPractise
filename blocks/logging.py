import datetime
import enum
import inspect
from blocks.filemanager import FileManager

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
    return datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")


def log(msg: str, status: LogStatus):
    blockname = get_block_name(inspect.currentframe().f_back)
    time = getNowTime()
    log_message = f"[{status.name}] [{time}] {blockname}: {msg}"
    fm.write_log(blockname, log_message)
    print(log_message)
