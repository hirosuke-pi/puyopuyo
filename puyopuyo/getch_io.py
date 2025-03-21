import os


class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        import msvcrt

        return msvcrt.getch()


def getchar():
    if os.name == "nt":
        impl = _GetchWindows()
    else:
        impl = _GetchUnix()

    return ord(impl())
