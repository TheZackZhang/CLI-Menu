import os
import sys

def get_char():
    """
    Read a single character from the keyboard, return entered character 
    immediately without waiting for the enter key
    """

    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    else:
        raise NotImplementedError(f'Unexpected platform: {sys.platform}')

def clear():
    """ Clear the terminal screen """
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """ Pause code execution until a key is pressed """
    print('Press any key to continue')
    get_char()