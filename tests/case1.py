from source.menu import Menu
from source.util import pause

def hello():
    print('hello')
    pause()

def world():
    print('world')
    pause()

sub_menu = Menu(
    options=[hello, world],
    exit_label='Return to Main Menu',
    title='Sub Menu',
)

main_menu = Menu(
    options={
        'Print Hello': hello,
        'Print World': world,
        'Sub Menu': sub_menu.loop,
    },
    title='Main Menu',
)

main_menu.loop()