import os
import sys
import logging
from pathlib import Path


class _LogFormatter(logging.Formatter):
    """
    Based on:                                                                  
    https://stackoverflow.com/a/13733863/1976617                               
    https://uran198.github.io/en/python/2016/07/12/colorful-python-logging.html
    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors                      
    """
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m", # bright/bold magenta
        logging.ERROR:    "\033[1;31m", # bright/bold red
        logging.WARNING:  "\033[1;33m", # bright/bold yellow
        logging.INFO:     "\033[0;37m", # white / light gray
        logging.DEBUG:    "\033[1;30m"  # bright/bold dark gray
    }
    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(_LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on  = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on  = ""
            record.color_off = ""
        return super(_LogFormatter, self).format(record, *args, **kwargs)


def _set_up_logging(
        console_log_output, 
        console_log_level, 
        console_log_color, 
        logfile_file, 
        logfile_log_level, 
        logfile_log_color, 
        log_console_template,
        log_file_template
    ):
    """
    Based on:                                                                  
    https://stackoverflow.com/a/13733863/1976617                               
    https://uran198.github.io/en/python/2016/07/12/colorful-python-logging.html
    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors                      
    """


    # Create logger
    # For simplicity, we use the root logger, i.e. call 'logging.getLogger()'
    # without name argument. This way we can simply use module methods for
    # for logging throughout the script. An alternative would be exporting
    # the logger, i.e. 'global logger; logger = logging.getLogger("<name>")'
    logger = logging.getLogger("enerplex-api")

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_log_output = console_log_output.lower()
    if (console_log_output == "stdout"):
        console_log_output = sys.stdout
    elif (console_log_output == "stderr"):
        console_log_output = sys.stderr
    else:
        print("Failed to set console output: invalid output: '%s'" % console_log_output)
        return False

    console_handler = logging.StreamHandler(console_log_output)

    # Set console log level
    try:
        console_handler.setLevel(console_log_level.upper()) # only accepts uppercase level names
    except:
        print("Failed to set console log level: invalid level: '%s'" % console_log_level)
        return False

    # Create and set formatter, add console handler to logger
    console_formatter = _LogFormatter(fmt=log_console_template, color=console_log_color)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create log file handler
    if logfile_file:
        try:
            logfile_handler = logging.FileHandler(logfile_file)
        except Exception as exception:
            print("Failed to set up log file: %s" % str(exception))
            return False

        # Set log file log level
        try:
            logfile_handler.setLevel(logfile_log_level.upper()) # only accepts uppercase level names
        except:
            print("Failed to set log file log level: invalid level: '%s'" % logfile_log_level)
            return False

        # Create and set formatter, add log file handler to logger
        logfile_formatter = _LogFormatter(fmt=log_file_template, color=logfile_log_color)
        logfile_handler.setFormatter(logfile_formatter)
        logger.addHandler(logfile_handler)

    return logger


logger: logging.Logger = None

if not logger:
    production = True
    log_path = Path("log/enerplex")
    os.makedirs(log_path, exist_ok=True)

    logger = _set_up_logging(
        console_log_output="stdout",
        console_log_level="warning" if production else "debug",
        console_log_color=True,
        logfile_file=os.path.join(log_path, "enerplex_api.log"), 
        logfile_log_level="debug",
        logfile_log_color=False,
        log_console_template="%(color_on)s[ENERPLEX-API] %(message)s%(color_off)s",
        log_file_template="%(color_on)s[%(asctime)s] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s"
    )

    if not production:
        logger.info(f"Starting api logger in development mode using level 'debug'")
