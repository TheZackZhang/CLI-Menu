import datetime as dt
from enum import Enum, auto
from typing import Any, Callable, Union

from .util import get_char


class InputType(int, Enum):
    single_key = auto()
    """ 
    return a single key entered from the keyboard immediately 
    without waiting for the Enter key
    """

    string = auto()
    """
    return all keys entered from the keyboard until Enter key is entered  
    """


class Prompt:

    def __init__(
        self,
        msg: Union[str, Callable[[], str]],
        input_type: InputType = InputType.string,
    ) -> None:
        """
        A while-loop that prompt for user-input until `self._exit` is set to True

        Parameters
        ----------
        msg:
            a string, or a no-arg-function that returns a string. 
            such string is printed out each loop

        input_type:
            whether to read a single key, or read all keys up until the Enter key
        """

        self.msg = msg
        self.input_type = input_type

    def loop(self):
        self._exit = False
        while not self._exit:
            self.print_message()
            command = self.prompt_input()
            command = self.pre_callback(command)
            returned = self.callback(command)
            returned = self.post_callback(returned)
        return returned

    def print_message(self):
        msg = self.msg
        if callable(msg):
            msg()
        else:
            print(msg, end='', flush=True)

    def prompt_input(self):
        t = self.input_type
        if t == InputType.single_key:
            key = get_char()
            print(key)
            return key
        elif t == InputType.string:
            return input()
        else:
            raise NotImplementedError(f'Unexpected input type: {t}')

    def pre_callback(self, command: str) -> str:
        """ 
        Overwrite this method to add extra logic
        on user-input before its passed to the callback 
        """
        return command

    def callback(self, command: str) -> Any:
        """
        Overwrite this method to alter the logic
        how user-input is processed 
        """
        self._exit = True
        return command

    def post_callback(self, returned: Any) -> Any:
        """
        Overwrite this method to add extra logic
        on the object returned from the callback 
        """
        return returned


class DatePrompt(Prompt):

    def callback(self, command: str) -> Any:

        formats = [
            '%m/%d/%Y',
            '%m-%d-%Y',
            '%m %d %Y',
            '%Y/%m/%d',
            '%Y-%m-%d',
            '%Y %m %d',
        ]

        for format_ in formats:
            try:
                date = dt.datetime.strptime(command, format_)
                self._exit = True
                return date
            except ValueError as e:
                pass

        print(
            f'Unexpected input: {command}. '
            f'Expecting date string of format "MM/DD/YYYY"'
        )
