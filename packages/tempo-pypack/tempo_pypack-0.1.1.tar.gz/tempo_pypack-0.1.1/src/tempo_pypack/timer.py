from time import sleep 
import sys

# Usage Example
# timer(5, preffix='Faltam', suffix='segundos.', separator=' ', close=False, text='Fim do timer!')

def timer(number: int, prefix: str = '', suffix: str = '', separator: str = '', close: bool = False, text: str = None):
    """Display a countdown timer in the terminal.

    This function prints a countdown timer that updates in place within the terminal, 
    optionally displaying a prefix, suffix, and custom separator. It can also print a 
    final message and optionally exit the program when completed.

    Args:
        number (int): The starting number for the countdown (e.g., 10 for a 10-second countdown).
        preffix (str, optional): A string to display before the countdown number. Defaults to ''.
        suffix (str, optional): A string to display after the countdown number. Defaults to ''.
        separator (str, optional): A separator to place between the preffix, number, and suffix. Defaults to ''.
        exit (bool, optional): If True, exits the program with `sys.exit()` after the countdown completes. Defaults to False.
        text (str, optional): An optional message to display after the countdown finishes. Defaults to None.


    Note:
        The timer uses `sys.stdout.write()` and `sys.stdout.flush()` to update the same line continuously.
        If `exit=True`, the program will terminate after the countdown completes.
    """

    formatted_preffix = f'{prefix}{separator}' if prefix else ''
    formatted_suffix = f'{separator}{suffix}' if suffix else ''

    contador = number
    while contador >= 0:
        sleep(1)
        sys.stdout.write(f'\r{formatted_preffix}{contador}{formatted_suffix} ')
        sys.stdout.flush()
        contador -= 1
    sys.stdout.flush()

    if text:
        print('\n', text, sep='')

    if close:
        sys.exit()
