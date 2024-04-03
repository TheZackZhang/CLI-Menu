from source.menu import Menu
from source.util import pause

def hello():
    """ Print hello """
    print('hello')
    pause()

def world():
    """ Print world """
    print('world')
    pause()

sub_menu = Menu(
    options=[hello, world],
    exit_label='Return to Main Menu',
    title='Main Menu -> Sub Menu',
)

main_menu = Menu(
    options=[hello, world, sub_menu.loop],
    labels=['Print Hello', 'Print World', 'Sub Menu'],
    title='Main Menu',
    use_docstring=False,
)

main_menu.loop()