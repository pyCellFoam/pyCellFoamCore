"""
Change the basic logging configuration to a more usable style.
Also use different colors for different logging levels. The first
parameter defines the minimal level for messages to be displayed. During
development, :code:`logging.DEBUG` is recommended. During production,
setting it to :code:`logging.INFO` will enhance performance by reducing
the number of messages.

Example usage:

.. code-block:: python

    # import
    from functions_lib.logging_formatter import set_logging_format

    # Configure logging
    set_logging_format(logging.DEBUG)

    # Some test messages
    logging.debug('Debug')
    logging.info('Info')
    logging.warning('Warning')
    logging.error('Test')
    logging.critical('Critical')

The output can also be written to a file:

.. code-block:: python

    # import
    from functions_lib.logging_formatter import set_logging_format

    # Configure logging
    set_logging_format(logging.DEBUG, filename="my_log.log")

If you want to retain the colors, you can write it to an ansi file and
use an editor that can display the colors, e.g. vscode with extension
`ANSI Colors <https://marketplace.visualstudio.com/items?itemName=iliazeus.vscode-ansi>`_.


.. code-block:: python

    # import
    from functions_lib.logging_formatter import set_logging_format

    # Configure logging
    set_logging_format(logging.DEBUG, filename="my_log.ansi")

If you want to write the output to the console and a file, you can use
the double_output parameter:

.. code-block:: python

    # import
    from functions_lib.logging_formatter import set_logging_format

    # Configure logging
    set_logging_format(logging.DEBUG, filename="my_log.log", double_output=True)

You can define different levels for the console and the file by giving
a list as the first parameter. The first element of the list is the
level for the logging file, the second element for the console output:

.. code-block:: python

    # import
    from functions_lib.logging_formatter import set_logging_format

    # Configure logging
    set_logging_format(
        [logging.WARNING, logging.DEBUG],
        filename="my_log.log",
        double_output=True,
    )

    # Some test messages
    logging.debug('Debug')  # Only goes to console
    logging.info('Info')  # Only goes to console
    logging.warning('Warning')  # Goes to console and log file
    logging.error('Test')  # Goes to console and log file
    logging.critical('Critical')  # Goes to console and log file

"""  # noqa: E501

import logging
from logging.handlers import RotatingFileHandler
import pathlib
from datetime import datetime
import time


def rreplace(s, old, new, occurrence):
    """
    Replace the last `occurrence` occurrences of a substring with a new
    string.

    Parameters
    ----------
    s : str
        The original string.
    old : str
        The substring to be replaced.
    new : str
        The string to replace the substring with.
    occurrence : int
        The number of occurrences to replace, starting from the end of
        the string.

    Returns
    -------
    str
        The modified string with the specified replacements applied.

    Examples
    --------
    >>> rreplace("hello world world", "world", "Python", 1)
    'hello world Python'
    >>> rreplace("a-b-c-d", "-", ":", 2)
    'a-b:c:d'

    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


class CustomFormatter(logging.Formatter):
    """
    Custom logging class

    """
    white = "\u001b[38;5;15m"
    grey = "\u001b[38;5;8m"
    yellow = "\u001b[38;5;11m"
    red = "\u001b[38;5;9m"
    magenta = "\u001b[38;5;13m"
    reset = "\x1b[0m"

    def __init__(self, log_format, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FORMATTERS = {
            logging.DEBUG: logging.Formatter(
                CustomFormatter.grey + log_format + CustomFormatter.reset
            ),
            logging.INFO: logging.Formatter(
                CustomFormatter.white + log_format + CustomFormatter.reset
            ),
            logging.WARNING: logging.Formatter(
                CustomFormatter.yellow + log_format + CustomFormatter.reset
            ),
            logging.ERROR: logging.Formatter(
                CustomFormatter.red + log_format + CustomFormatter.reset
            ),
            logging.CRITICAL: logging.Formatter(
                CustomFormatter.magenta + log_format + CustomFormatter.reset
            ),
        }

    def format(self, record):
        formatter = self.FORMATTERS.get(record.levelno)
        return formatter.format(record)


class RotatingFileHandlerTimestamp(RotatingFileHandler):
    """
    RotatingFileHandler with timestamp in filename

    """
    def __init__(self, filename, **kwargs):
        self.base_filename = filename
        # super().__init__(filename, **kwargs)
        super().__init__(self.get_filename(), **kwargs)

    def get_filename(self):
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
        return rreplace(self.base_filename, ".log", f"_{now}.log", 1)

    def doRollover(self):
        """
        Override doRollover to add timestamp to filename

        """
        self.stream.close()
        self.stream = self._open()
        self.baseFilename = self.get_filename()


def set_logging_format(
        level: int = logging.INFO,
        filename: str = None,
        filemode: str = "w",
        double_output: bool = False,
        color_console: bool = True,
        color_file: bool | None = None,
        log_format_console: str = "%(filename)30s : %(lineno)5d : %(funcName)20s : %(levelname)8s : %(message)s",  # noqa: E501
        log_format_file: str = "%(asctime)s : %(filename)30s : %(lineno)5d : %(funcName)20s : %(levelname)8s : %(message)s",  # noqa: E501
        rotating: bool = False,
        use_timestamp_for_rotation: bool = False,
        **kwargs,
):
    """Set logging format

    Parameters
    ----------
    level : int, optional
        Some integer value for the minimal log level to be displayed, by
        default logging.INFO
    filename : str, optional
        Give a filename to write the output into this file instead of
        the console, by default None
    filemode : str, optional
        This parameter is directly passed to the basicConfig method and
        is listed here only to overwrite the standard behavior "a" with
        "w", by default "w"
    double_output : bool, optional
        If True, the output is written to the console and the file, by
        default False
    color_console : bool, optional
        If True, the console output will be colorized, by default True
    color_file : bool or None, optional
        If True, the file output will be colorized. If None, the color
        will be determined based on the file extension, by default None
    log_format_console : str, optional
        The format string for console logging, by default
        "%(filename)30s : %(lineno)5d : %(funcName)20s : %(levelname)8s
        : %(message)s"
    log_format_file : str, optional
        The format string for file logging, by default "%(asctime)s :
        %(filename)30s : %(lineno)5d : %(funcName)20s : %(levelname)8s :
        %(message)s"
    rotating : bool, optional
        If True, the log file will be rotated, by default False
    use_timestamp_for_rotation : bool, optional
        If True, a timestamp will be added to the filename during
        rotation, by default False
    kwargs : dict, optional
        Parameters to be passed to basicConfig
    """
    if rotating and filename is None:
        raise ValueError("rotating requires a filename")

    if filename is not None:
        filepath = pathlib.Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(level, list):
        level_0 = level[0]
        level_1 = level[1]
    else:
        level_0 = level
        level_1 = level

    if not isinstance(level_0, int) or not isinstance(level_1, int):
        raise TypeError(
            "level must be an integer or a list of integers, but got", level
        )

    logging.basicConfig(
         level=level_0,
         force=True,
         filename=filename if not rotating else None,
         filemode=filemode,
         encoding="utf-8",
         **kwargs,
     )

    if color_file is None and filename is not None:
        color_file = filename.endswith(".ansi")

    if double_output:

        # If two handlers are in use, the level of the logger must be
        # unset so that all messages go to the logger and the handlers
        # can decide which message to display

        logging.getLogger().setLevel(logging.NOTSET)
        logging.getLogger().handlers[0].setLevel(level_0)

        ch = logging.StreamHandler()
        ch.setLevel(level_1)

        if color_console:
            ch.setFormatter(CustomFormatter(log_format_console))
        else:
            ch.setFormatter(logging.Formatter(log_format_console))
        logging.getLogger().addHandler(ch)

    if filename is None:
        if color_console:
            logging.getLogger().handlers[0].setFormatter(
                CustomFormatter(log_format=log_format_console)
            )
        else:
            logging.getLogger().handlers[0].setFormatter(
                logging.Formatter(log_format_console)
            )
    else:
        if rotating:
            if use_timestamp_for_rotation:
                rfh = RotatingFileHandlerTimestamp(
                    filename,
                    maxBytes=5_000_000,
                    backupCount=10_000,
                )
            else:
                rfh = RotatingFileHandler(
                    filename,
                    maxBytes=5_000_000,
                    backupCount=10_000,
                )

            rfh.setLevel(level_0)

            logging.getLogger().handlers[0] = rfh
        if color_file:
            logging.getLogger().handlers[0].setFormatter(
                CustomFormatter(log_format=log_format_file)
            )
        else:
            logging.getLogger().handlers[0].setFormatter(
                logging.Formatter(log_format_file)
            )


if __name__ == '__main__':

    # Configure logging
    set_logging_format(
        [logging.WARNING, logging.DEBUG],
        filename="logs/my_log.log",
        double_output=True,
        use_timestamp_for_rotation=True,
        rotating=True,

    )

    # Some test messages
    logging.debug('Debug')
    logging.info('Info')
    logging.warning('Warning')
    logging.error('Error')
    logging.critical('Critical')

    # Create logger to set different logging level
    _log = logging.getLogger(__name__)
    _log.setLevel(logging.INFO)

    # Some test messages in logger instance
    _log.debug("Debug in logger")
    _log.info("Info in logger")

    for i in range(100):
        _log.error("Test %s", i)
        time.sleep(0.01)
