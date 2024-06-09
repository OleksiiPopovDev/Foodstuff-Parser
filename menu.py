import keyboard
import os
from pynput.keyboard import Key, Listener



selected = 1


def show_menu(clear_screen: bool = True):
    global selected
    if clear_screen == True:
        print('\033c')

    print("Choose an option:\n")
    for i in range(1, 5):
        print("\t{1} {0}. Do something {0} {2}".format(i, "\033[1;33m>\033[1;34m" if selected == i else " ",
                                                     "\033[1;33m<\033[0m" if selected == i else " "))
    print('\r')

def up():
    global selected
    if selected == 1:
        return
    selected -= 1
    show_menu()


def down():
    global selected
    if selected == 4:
        return
    selected += 1
    show_menu()


def enter():
    global selected
    print('\r\n\n\n\nChoose menu #%d\n\n\n\n\n\n' % selected)




# keyboard.add_hotkey('up', up)
# keyboard.add_hotkey('down', down)
# keyboard.add_hotkey('enter', enter)
# keyboard.wait('esc')


def show(key):
    if key == Key.up:
        up()

    if key == Key.down:
        down()

    if key == Key.enter:
        enter()
        show_menu(clear_screen=False)

    if key == Key.delete:
        # Stop listener
        exit()


# Collect all event until released
with Listener(on_release=show) as listener:
    show_menu()
    listener.join()
