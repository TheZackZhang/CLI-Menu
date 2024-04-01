from typing import Callable, Dict, List, Union

from .util import get_char, clear, pause

Label = str
OptionCallback = Callable[[], None]

NUMBERS = [str(i) for i in range(1, 10)]
LETTERS = [chr(i) for i in range(ord('a'), ord('z')+1)]
OPTION_KEYS = NUMBERS + LETTERS
EXIT_KEY = '0'

H_BAR = '-' * 20

class Menu:

    def __init__(
        self, 
        options: Union[List[OptionCallback], Dict[Label, OptionCallback]], 
        exit_label: Label = None,
        title: str = None,
        prompt: str = None,
        indent: str = None
    ) -> None:
        """
        CLI menu with options that can be triggered by a keyboard key-press  

        Each option has 3 components:
        - key: 
            single-character that would trigger the callback 
        - label: 
            string label of the option
        - callback: 
            function that gets called. it should take no args and return None
            (no args and return value are passed back-n-forth)

        """
        self.set_options(options, exit_label, indent)
        self.title = title or 'Menu'
        self.prompt = prompt or f'Enter an option {self.keys_str}: '

    def set_options(
        self, 
        options: Union[List[OptionCallback], Dict[Label, OptionCallback]],
        exit_label: str = None,
        indent: str = None,
    ):
        if len(options) > len(OPTION_KEYS):
            raise ValueError(f'Cannot have more than {len(OPTION_KEYS)} options: {options}')

        if isinstance(options, list):
            labels = [func.__name__ for func in options]
            funcs = options

        elif isinstance(options, dict):
            labels = list(options.keys())
            funcs = list(options.values())

        else:
            raise NotImplementedError(f'Unexpected type: {type(options)}')
        
        labels = {key: label for key, label in zip(OPTION_KEYS, labels)}
        funcs = {key: func for key, func in zip(OPTION_KEYS, funcs)}

        labels[EXIT_KEY] = exit_label or 'Exit'
        funcs[EXIT_KEY] = self.exit

        indent = indent or '  '

        str_labels = '\n'.join(
            f'{indent}<{key}> {label}' 
            for key, label in labels.items()
        )
        str_keys = f'({', '.join(labels)})'

        self.labels = labels
        self.funcs = funcs
        self.labels_str = str_labels
        self.keys_str = str_keys

    def print(self):
        msg = [
            self.title,
            H_BAR,
            self.labels_str,
            H_BAR,
            self.prompt,
        ]
        msg = [i for i in msg if i is not None]
        msg = '\n'.join(msg)
        print(msg, end='', flush=True)

    def dispatch(self, key: str):
        print(key)
        d = self.funcs
        f = d.get(key, self.default)
        f()

    def default(self):
        """ Default callback for undefined key """
        print(f'Unexpected option key. Expecting: {self.keys_str}')
        pause()

    def exit(self):
        self._loop = False

    def loop(self):
        self._loop = True
        while self._loop:
            clear()
            self.print()
            key = get_char()
            self.dispatch(key)