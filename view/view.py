import os
from view.color import Color
import signal
import sys


class View:
    COLOR_DEFAULT: str = '\033[0m'
    COLOR_PURPLE: str = '\033[0;35m'
    COLOR_YELLOW: str = '\033[1;33m'
    COLOR_CYAN: str = '\033[0;36m'
    COLOR_RED: str = '\033[0;31m'
    COLOR_BLUE: str = '\033[0;34m'
    COLOR_L_GREEN: str = '\033[1;32m'
    COLOR_L_BLUE: str = '\033[1;34m'

    __menu_items: list[str]

    selected_menu: int = 0

    def __init__(self, menu: list[str]) -> None:
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        self.__menu_items = menu
        self.show_banner()
        self.show_menu()

    def show_banner(self) -> None:
        print(
            "\n\t _______                 __ ______\n" +
            self.paint(
                "\t|    ___|.-----.-----.--|  |   __ \\.---.-.----.-----.-----.----. {Yellow}v%s{ColorOff}\n"
                % os.getenv('VERSION')
            ) +
            "\t|    ___||  _  |  _  |  _  |    __/|  _  |   _|__ --|  -__|   _|\n" +
            "\t|___|    |_____|_____|_____|___|   |___._|__| |_____|_____|__|\n"
        )
        print(self.paint("\t\t{Purple}Author:\t{ColorOff}%s" % os.getenv('AUTHOR_NAME')))
        print(self.paint("\t\t{Purple}E-mail:\t{ColorOff}%s" % os.getenv('AUTHOR_EMAIL')))

    def show_menu(self) -> None:
        print(self.COLOR_DEFAULT)
        count: int = 0
        for item in self.__menu_items:
            print(self.paint("\t\t{Red}[{Yellow}%d{Red}]\t{Cyan}%s" % (count, item)))
            count += 1
        print(self.COLOR_DEFAULT)
        self.propose_choose()

    def propose_choose(self) -> None:
        try:
            self.selected_menu = int(input(self.paint("\t\t{Green}Choose menu number {BGreen}>> ")))
        except (ValueError, KeyboardInterrupt):
            self.selected_menu = 0

    def separator(self) -> None:
        print("%s-" % self.COLOR_DEFAULT * 100)

    @staticmethod
    def paint(string: str) -> str:
        for color in Color:
            string = string.replace("{%s}" % color.name, color.value)

        return string

    @staticmethod
    def count_biggest_line(list_items: list) -> int:
        biggest_line_length: int = 0
        for item in list_items:
            name_length = len(item)
            biggest_line_length = name_length if name_length > biggest_line_length else biggest_line_length

        return biggest_line_length

    @staticmethod
    def add_spaces_for_line_up(line: str, count_biggest_line: int) -> str:
        more_spaces: int = count_biggest_line - len(line)
        return line + ' ' * more_spaces

    @staticmethod
    def get_count_spaces_for_line_up(line: str, count_biggest_line: int) -> int:
        return count_biggest_line - len(line)
