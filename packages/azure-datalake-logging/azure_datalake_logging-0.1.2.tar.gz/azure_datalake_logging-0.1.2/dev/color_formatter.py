import logging
from typing import Dict, Optional


class ColorFormatter(logging.Formatter):
    """
    Custom formatter that adds color to log messages based on their level.

    Colors are applied only when outputting to a terminal.
    """

    # ANSI color codes
    COLORS: Dict[int, str] = {
        logging.DEBUG: "\033[38;5;246m",  # Gray
        logging.INFO: "\033[38;5;39m",    # Blue
        logging.WARNING: "\033[38;5;208m", # Orange
        logging.ERROR: "\033[38;5;196m",   # Red
        logging.CRITICAL: "\033[48;5;196;38;5;231m", # White on Red
    }
    RESET: str = "\033[0m"

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        use_colors: bool = True
    ) -> None:
        """
        Initialize the formatter with optional color support.

        Args:
            fmt: Format string
            datefmt: Date format string
            use_colors: Whether to apply colors (default: True)
        """
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors based on level.

        Args:
            record: The log record to format

        Returns:
            Formatted log message with appropriate colors
        """
        # Make a copy to avoid modifying the original
        record_copy = logging.makeLogRecord(record.__dict__)

        # Apply color if enabled
        if self.use_colors:
            color = self.COLORS.get(record.levelno, self.RESET)
            record_copy.levelname = f"{color}{record.levelname}{self.RESET}"
            record_copy.msg = f"{color}{record.msg}{self.RESET}"

        return super().format(record_copy)