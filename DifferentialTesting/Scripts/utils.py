from typing import TextIO


class MyLogger(TextIO):
    """
        Simple logger class.

        Writes to log file and stdout.

        :param log_file: Path to log file. If None, prints to stdout only.
        :param buffering: Buffering mode for log file. Default is -1 (unbuffered).
    """
    def __init__(self,log_file:str=None,buffering:int=-1):
        if log_file is None:
            self.log_file = None
        else:
            self.log_file=open(log_file,'w',buffering)

    def __del__(self):
        if self.log_file is not None:
            self.log_file.close()

    def write(self, msg:str):
        if self.log_file is not None:
            self.log_file.write(msg)
        print(msg,end='')