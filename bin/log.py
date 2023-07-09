from enum import Enum

SEPERATOR_LENGTH = 60


class LogType(Enum):
    INFO = 1
    SUCCESS = 2
    WARN = 3
    ERROR = 4


def log(message: str, target_log_type: LogType = LogType.INFO, end: bool = True) -> None:
    """
    output to console `message` with prefix of `target_log_type` name wrapped in square brackets and equally spaced.
    """
    message_type = target_log_type.name
    for log_type in LogType:
        if log_type.value == target_log_type.value:
            message_type = log_type.name
            break

    if end:
        print(f' [{message_type}]{(10 - len(message_type)) * " "}- {message}')
    else:
        print(
            f' [{message_type}]{(10 - len(message_type)) * " "}- {message}', end='')


def print_seperator(seperator_length: int = SEPERATOR_LENGTH):
    """
    print a standard seperator, with a desired length of `seperator_length`.
    """
    print(f'{"-" * seperator_length}')
