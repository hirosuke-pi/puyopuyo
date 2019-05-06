import os, sys
import random

from puyo_base import *
from getch_io import *
from graphics import *


def main():
    if os.name == "nt":
        os.system("title CUI Graphic PuyoPuyo!")
    reset_color()
    while True:
        space = "    "
        color_val = 4
        color_party = "RGYBMCW"
        str_color1 = random.choice(color_party)
        str_color2 = random.choice(color_party)
        str_color3 = random.choice(color_party)
        str_color4 = random.choice(color_party)

        game_display = [
            [[space, "n", "n"], ["    pppppppp                                 ", str_color1, ""], ["                      ", str_color4, ""]],
            [[space, "n", "n"], ["     pp    pp             yy      yy         ", str_color1, ""], ["       OOOOOOOOOO       ", str_color4, ""]],
            [[space, "n", "n"], ["    pp   pp             yy yy   yyy     oooo ", str_color1, ""], ["     OO          OO   ", str_color4, ""]],
            [[space, "n", "n"], ["   pppppp    uu   uu      yy   yyy    oo   oo", str_color1, ""], ["    OO   |    |   OO", str_color4, ""]],
            [[space, "n", "n"], ["  pp        uu   uu         yyy yy   oo   oo ", str_color1, ""], ["    OO            OO   ", str_color4, ""]],
            [[space, "n", "n"], [" pp          uuuuu uu   yy     yy     oooo   ", str_color1, ""], ["      OOOOOOOOOOOO", str_color4, ""]],
            [[space, "n", "n"], ["                          yyyyyy             ", str_color1, ""], ["     ", str_color4, ""]],
            [[space * 3, "n", "n"], ["    pppppppp                                      ", str_color2, ""], ["", str_color3, ""]],
            [[space * 3, "n", "n"], ["     pp    pp             yy      yy              ", str_color2, ""], ["!!!", str_color3, ""]],
            [[space * 3, "n", "n"], ["    pp   pp             yy yy   yyy     oooo     ", str_color2, ""], ["!!!", str_color3, ""]],
            [[space * 3, "n", "n"], ["   pppppp    uu   uu      yy   yyy    oo   oo   ", str_color2, ""], ["!!!", str_color3, ""]],
            [[space * 3, "n", "n"], ["  pp        uu   uu         yyy yy   oo   oo   ", str_color2, ""], ["!!", str_color3, ""]],
            [[space * 3, "n", "n"], [" pp          uuuuu uu   yy     yy     oooo   ", str_color2, ""], ["", str_color3, ""]],
            [[space * 3, "n", "n"], ["                          yyyyyy             ", str_color2, ""], ["!!", str_color3, ""]],
        ]

        clear()
        print("\r\n")
        cprint(game_display)
        print("\r\n")
        print("     [*] Key-layout: [A]...Left, [S]...Down, [D]...Right")
        print("                     [L]...Left-Turn, [M]...Right-Turn, [Enter]...Exit")

        print("\r\n")
        puyo_color = input("     [?] Please input the number of puyo-color. (2~5): ")

        if puyo_color.isdigit():
            color_val = int(puyo_color)

            if color_val == 0:
                print()
                break
            elif color_val < 2 or color_val > 5:
                continue
        else:
            continue
        
        print("\r\n     [+] Press Enter to start!")
        input()

        while True:
            puyo_game = PuyoPuyoPlay()
            puyo_game.play(color_val)

            print("\r\n    [!] GameOver!")
            y_n = input("    [?] Do you want to play one more time? (y/n): ")  
            if y_n.lower() != "y":
                break


if __name__ == "__main__":
    main()
