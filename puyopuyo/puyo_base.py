import copy
import os
import threading
import time

from .getch_io import *
from .puyo_system import *


class PuyoPuyoPlay:

    def __init__(self):
        self.__exit_flag = True
        self.__gameover = False
        self.__puyo_active = True
        self.__gboard = GraphicBoard()

    def play(self, puyo_color_val=4):
        # I/O
        clear()
        hide_cursor()
        self.__gboard.set_next_puyo(puyo_color_val)
        ioth = threading.Thread(target=self.__move_puyo_aync)
        ioth.daemon = True
        ioth.start()
        while not (self.__gameover):
            char = getchar()
            if self.__gboard.moving_flag:
                if char == 97:  # A
                    self.__gboard.move_puyo(-1, 0)
                    self.__gboard.draw_ex()
                elif char == 115:  # S
                    self.__gboard.move_puyo(0, 1)
                    self.__gboard.score += 1
                    self.__gboard.draw_ex()
                elif char == 100:  # D
                    self.__gboard.move_puyo(1, 0)
                    self.__gboard.draw_ex()
                elif char == 108:  # L
                    self.__gboard.replace_puyo(True)
                    self.__gboard.draw_ex()
                elif char == 109:  # M
                    self.__gboard.replace_puyo(False)
                    self.__gboard.draw_ex()
                elif char == 32:
                    clear()
                    hide_cursor()

            # Enter
            if char == 13 or self.__gboard.check_gameover():
                break

        show_cursor()
        self.__exit_flag = False
        ioth.join()

    def __move_puyo_aync(self):
        self.__gboard.puyo = self.__gboard.make_next_puyo()
        self.__gboard.puyo1 = self.__gboard.make_next_puyo()
        self.__gboard.puyo2 = self.__gboard.make_next_puyo()
        while self.__exit_flag:
            # Check puyo chains
            self.__gboard.chain_val = 0
            while True:
                puyo_chain = self.__gboard.check_puyo_chain()
                if len(puyo_chain) <= 0:
                    break
                self.__gboard.all_clear = False
                self.__gboard.remove_puyo(puyo_chain, True)
                self.__gboard.refresh_board()
                self.__gboard.chain_val += 1
                self.__gboard.max_chain_val = max(self.__gboard.max_chain_val, self.__gboard.chain_val)
                self.__gboard.calc_score(puyo_chain)
                self.__gboard.check_all_clear()
                self.__gboard.draw_ex()
                time.sleep(0.5)

            if self.__gboard.check_gameover():
                self.__gameover = True
                break

            # Initalize next puyo
            self.__gboard.puyo = copy.deepcopy(self.__gboard.puyo1)
            self.__gboard.puyo1 = copy.deepcopy(self.__gboard.puyo2)
            self.__gboard.puyo2 = self.__gboard.make_next_puyo()

            self.__gboard.add_puyo(self.__gboard.puyo)
            self.__gboard.draw_ex()
            self.__puyo_active = True
            self.__gboard.moving_flag = True
            # Fall puyo
            while self.__exit_flag and self.__puyo_active:
                self.__gboard.move_puyo(0, 1)
                time.sleep(0.9)
                self.__gboard.draw_ex()
                # Put puyo
                if not (self.__gboard.moving_flag):
                    while self.__exit_flag and self.__puyo_active:
                        self.__gboard.move_puyo(0, 1)
                        self.__gboard.draw_ex()
                        self.__puyo_active = self.__gboard.check_puyo_active(self.__gboard.puyo)
                        time.sleep(0.05)
                if not (self.__puyo_active):
                    break

    def stop(self):
        self.__exit_flag = True


def main():
    if os.name == "nt":
        os.system("title CUI Graphic PuyoPuyo!")

    puyo = PuyoPuyoPlay()
    puyo.play(4)

    print("\r\n    [!] GameOver. Press Enter to exit...")
    input()


if __name__ == "__main__":
    main()
