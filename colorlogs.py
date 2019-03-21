"""
Echo all input lines, colorizing any that
include common logging level indicators:
    DEBUG -> (none)
    TRACE -> (none)
    INFO -> bright white
    WARNING -> bright yellow
    ERROR -> bright red
    CRITICAL -> bright white on red
    FATAL -> bright white on red
"""

import sys


ESC = chr(27)

NORMAL = 0
BRIGHT = 1

FG_BLACK = 30
FG_RED = 31
FG_GREEN = 32
FG_YELLOW = 33
FG_BLUE = 34
FG_MAGENTA = 35
FG_CYAN = 36
FG_WHITE = 37

BG_BLACK = 40
BG_RED = 41
BG_GREEN = 42
BG_YELLOW = 43
BG_BLUE = 44
BG_MAGENTA = 45
BG_CYAN = 46
BG_WHITE = 47

FATAL_KEY = " - FATAL - "
CRITICAL_KEY = " - CRITICAL - "
ERROR_KEY = " - ERROR - "
WARNING_KEY = " - WARNING - "
INFO_KEY = " - INFO - "
TRACE_KEY = " - TRACE - "
DEBUG_KEY = " - DEBUG - "


def stdout(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def _ansi(*values):
    return f"{ESC}[{';'.join(map(str, values))}m"


def _reset():
    return _ansi(NORMAL)


def _color(string, *values):
    """Colors the given string with the given ANSI color index."""
    return f"{_ansi(*values)}{string}{_reset()}"


def red(string):
    return _color(string, FG_RED)


def green(string):
    return _color(string, FG_GREEN)


def blue(string):
    return _color(string, FG_BLUE)


def yellow(string):
    return _color(string, FG_YELLOW)


def black(string):
    return _color(string, FG_BLACK)


def debug(line):
    return line


def trace(line):
    return line


def info(line):
    return _color(line, FG_WHITE, BRIGHT)


def warning(line):
    return _color(line, FG_YELLOW, BRIGHT)


def error(line):
    return _color(line, FG_RED, BRIGHT)


def fatal(line):
    return _color(line, FG_WHITE, BG_RED, BRIGHT)


def critical(line):
    return _color(line, FG_WHITE, BG_RED, BRIGHT)


def test():
    for func in [red, green, blue, yellow, black]:
        stdout(func(func.__name__))
        stdout(" ")

    stdout("\n")

    for func in [debug, trace, info, warning, error, critical, fatal]:
        stdout(func(func.__name__))
        stdout(" ")


MAPPING = {
    FATAL_KEY: fatal,
    CRITICAL_KEY: critical,
    ERROR_KEY: error,
    WARNING_KEY: warning,
    INFO_KEY: info,
    TRACE_KEY: trace,
    DEBUG_KEY: debug,
}


def main():
    for line in sys.stdin:
        line = line[:-1]
        for (key, func) in MAPPING.items():
            if key in line:
                stdout(func(line))
                break
        else:
            stdout(line)
        stdout("\n")


if __name__ == '__main__':
    main()
