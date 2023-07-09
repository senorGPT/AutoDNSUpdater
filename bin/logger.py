from enum import Enum
import datetime

SEPERATOR_LENGTH = 60


class LogType(Enum):
    INFO = 1
    SUCCESS = 2
    WARN = 3
    ERROR = 4


class Logger():
    def __init__(self):
        self.file = open('log.txt', 'a')

    def __del__(self):
        self.file.close()

    def get_datetime_stamp(self) -> str:
        """
        return the current date and time in desired format as a str.
        """     
        current_time = datetime.datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")

    def close(self) -> None:
        """
        close the opened file for reading.
        """
        self.file.close()

    def write_to_file(self, message: str) -> None:
        """
        write to file `message`.
        """
        self.file.write(f'[{self.get_datetime_stamp()}]: {message}')

    def log(self, message: str, target_log_type: LogType = LogType.INFO, end: bool = True, prefix: bool = False) -> None:
        """
        output to console `message` with prefix of `target_log_type` name wrapped in square brackets and equally spaced.
        """
        prefix = ""
        if prefix:
            message_type = target_log_type.name
            for log_type in LogType:
                if log_type.value == target_log_type.value:
                    message_type = log_type.name
                    break
            prefix = f' [{message_type}]{(10 - len(message_type)) * " "}- '

        final_message = f'{prefix}{message}'
        if end:
            print(f'{final_message}')
            self.write_to_file(f'{final_message}\n')
        else:
            print(f'{final_message}', end='')
            self.write_to_file(f'{final_message}')


def print_seperator(seperator_length: int = SEPERATOR_LENGTH) -> None:
    """
    print a standard seperator, with a desired length of `seperator_length`.
    """
    print(f'{"-" * seperator_length}')
