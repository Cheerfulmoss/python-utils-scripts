"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

from datetime import datetime
from time import perf_counter_ns
import os


class DbgLog:
    def __init__(self, filename: str, debug_id, console_log: bool,
                 file_log: bool) -> None:
        self._filename = filename
        self._file_log = file_log
        self._console_log = console_log
        self._debug_id = debug_id

        self._check_valid()
        self._start_dbg = perf_counter_ns()
        self._seperator = "  ::  "
        format_log = self._make_line("=== START OF LOG ===", 1, self._debug_id)
        if self._file_log:
            self._log_file = open(f"{self._filename}.dbg", "a")
            self._log_file.write(f"{format_log}\n")
        if self._console_log:
            print(format_log)

    def _make_line(self, log: str, condition: int, accessory: any) -> str:
        line_start = (
            f"{datetime.now().strftime('%d/%m/%y-%H:%M:%S'): <17}"
            f"{self._seperator}"
        )
        if condition == 0:
            formatted_log = (f"{line_start}{log: <40}{self._seperator}"
                             f"{accessory: <20}")
        elif condition == 1:
            formatted_log = (f"{line_start}{log: ^40}{self._seperator}"
                             f"{accessory: <20}")
        else:
            raise ValueError("'condition' must be 0 or 1.")
        return formatted_log

    def _check_valid(self):
        for char in self._filename:
            if char in "!\"#%&'()*+,/:;<=>?[\\]^1{|}":
                raise ValueError("'filename' must only contain valid filename "
                                 "characters")
        if self._file_log not in [0, 1] or self._console_log not in [0, 1]:
            raise ValueError("'console_log' and 'file_log' must be either "
                             "True or false")

    @staticmethod
    def _format_time(time_ns: int):
        if time_ns >= (factor := 8.64 * 10 ** 13):
            time_d = round(time_ns / factor, 5)
            formatted_time = f"{time_d} days"
        elif time_ns >= (factor := 3.6 * 10 ** 12):
            time_h = round(time_ns / factor, 5)
            formatted_time = f"{time_h} hrs"
        elif time_ns >= (factor := 6 * 10 ** 10):
            time_m = round(time_ns / factor, 5)
            formatted_time = f"{time_m} mins"
        elif time_ns >= (factor := 10 ** 9):
            time_s = round(time_ns / factor, 5)
            formatted_time = f"{time_s} s"
        elif time_ns >= 10 ** 6:
            time_ms = round(time_ns / 10 ** 6, 5)
            formatted_time = f"{time_ms} ms"
        else:
            formatted_time = f"{time_ns} ns"
        return formatted_time

    def dbg_print(self, log: str, accessory: any = None):
        if accessory is None:
            accessory = ""
        format_log = self._make_line(log, 0, accessory)
        if self._file_log:
            self._log_file.write(f"{format_log}\n")
        if self._console_log:
            print(format_log)

    def dbg_close(self):
        end_dbg = self._format_time(perf_counter_ns() - self._start_dbg)
        format_log = self._make_line("=== END OF LOG ===", 1, end_dbg)
        if self._file_log:
            self._log_file.write(f"{format_log}\n")
        if self._console_log:
            print(format_log)

    def dbg_delete(self):
        if not self._log_file.closed:
            self._log_file.close()
        os.remove(f"{self._filename}.dbg")

    def dbg_clear(self):
        if not self._log_file.closed:
            self._log_file.close()
        clear_file = open(f"{self._filename}.dbg", "w")
        clear_file.close()


if __name__ == "__main__":
    log = DbgLog("test", 83, True, True)
    for i in range(10):
        log.dbg_print("Hello World", f"Test {i + 1}")
    log.dbg_close()
    log.dbg_delete()
