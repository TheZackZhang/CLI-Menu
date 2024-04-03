from typing import Callable, List, TypeVar

from .util import clear, pause
from .prompt import Prompt, InputType
import string

OptionCallback = Callable[[], None]
""" a function that takes no arguments and return nothing """

Char = TypeVar('Char', bound=str)
""" a single character """

KEYS = string.digits + string.ascii_letters


class Menu(Prompt):

    def __init__(
        self,
        options: List[OptionCallback],
        labels: List[str] = None,
        keys: List[Char] = None,
        title: str = None,
        prompt: str = None,
        exit_key: str = None,
        exit_label: str = None,
        indent: str = None,
        h_bar: str = None,
        use_docstring: bool = None,
    ) -> None:
        """
        A CLI menu with options that are callbed based on user key-press  

        Each option has 3 components:
        - key: 
            single-character that would trigger the callback 
        - label: 
            string label of the option
        - callback: 
            function that gets called for the corresponding key
            (no args and return value are passed back-n-forth)
        """

        self.input_type = InputType.single_key
        self.setup(options, labels, keys, title, prompt, exit_key,
                   exit_label, indent, h_bar, use_docstring)

    def setup(
        self,
        options: List[OptionCallback],
        labels: List[str] = None,
        keys: List[Char] = None,
        title: str = None,
        prompt: str = None,
        exit_key: str = None,
        exit_label: str = None,
        indent: str = None,
        h_bar: str = None,
        use_docstring: bool = None,
    ):

        if len(options) > (len(KEYS)-1):
            raise ValueError(
                f'Cannot have more than {(len(KEYS)-1)} options: {options}')

        title = title or "Menu"
        prompt = prompt or 'Enter an option: '
        exit_key = exit_key or '0'
        exit_label = exit_label or 'Exit'
        indent = indent or '  '
        h_bar = h_bar or '--------------------'
        use_docstring = use_docstring if use_docstring is not None else True

        keys = keys or [key for key in KEYS if key != exit_key][:len(options)]
        labels = labels or [func.__name__ for func in options]

        for key in [*keys, exit_key]:
            if key not in KEYS:
                raise ValueError(f'Unexpected key: {key}')

        keys.append(exit_key)
        labels.append(exit_label)

        d_options = dict(zip(keys, options))

        msg_lines = [
            f'{indent}{key} {label}'
            for key, label in zip(keys, labels)
        ]

        if use_docstring:
            for i, option in enumerate(options):
                if option.__doc__:
                    msg_lines[i] += f'\n{indent*2}{option.__doc__}'

        msg = '\n'.join([
            title,
            h_bar,
            *msg_lines,
            h_bar,
            prompt,
        ])

        self.options = options
        self.labels = labels
        self.keys = keys
        self.title = title
        self.prompt = prompt
        self.indent = indent
        self.exit_key = exit_key
        self.exit_label = exit_label
        self.h_bar = h_bar
        self.use_docstring = use_docstring

        self.d_options = d_options
        self.msg = msg

    def print_message(self):
        clear()
        return super().print_message()

    def callback(self, command: str) -> str:
        key = command
        if key == self.exit_key:
            self._exit = True
        elif key in self.d_options:
            self.d_options[key]()
        else:
            print(f'Unexpected key: {key}. Expecting: {", ".join(self.keys)}')
            pause()
        return command

