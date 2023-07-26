import os


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
        self.__menu_items = menu
        self.separator()
        self.show_banner()
        self.separator()
        self.show_menu()

    def show_banner(self) -> None:
        print(
            "\n\t _______                 __ ______\n" +
            "\t|    ___|.-----.-----.--|  |   __ \\.---.-.----.-----.-----.----.\t%sv%s%s\n" %
            (self.COLOR_YELLOW, os.getenv('VERSION'), self.COLOR_DEFAULT) +
            "\t|    ___||  _  |  _  |  _  |    __/|  _  |   _|__ --|  -__|   _|\n" +
            "\t|___|    |_____|_____|_____|___|   |___._|__| |_____|_____|__|\n"
        )
        print("\t\t%sAuthor:\t%s%s" % (self.COLOR_PURPLE, self.COLOR_DEFAULT, os.getenv('AUTHOR_NAME')))
        print("\t\t%sE-mail:\t%s%s" % (self.COLOR_PURPLE, self.COLOR_DEFAULT, os.getenv('AUTHOR_EMAIL')))

    def show_menu(self) -> None:
        print(self.COLOR_DEFAULT)
        count: int = 0
        for item in self.__menu_items:
            print("\t\t%s[%s%d%s]\t%s%s" % (
                self.COLOR_RED, self.COLOR_YELLOW, count, self.COLOR_RED, self.COLOR_CYAN, item))
            count += 1
        print(self.COLOR_DEFAULT)
        self.separator()
        self.propose_choose()

    def propose_choose(self) -> None:
        try:
            self.selected_menu = int(input("\t\t%sChoose menu number: " % self.COLOR_L_GREEN))
        except (ValueError, KeyboardInterrupt):
            self.selected_menu = 0

    def separator(self) -> None:
        print("%s-" % self.COLOR_DEFAULT * 100)
