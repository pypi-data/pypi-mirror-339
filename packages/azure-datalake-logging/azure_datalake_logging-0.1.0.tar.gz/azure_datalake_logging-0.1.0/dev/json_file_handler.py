import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class JsonFileHandler(logging.Handler):
    """
    Custom logging handler that writes log records as JSON to a file.

    Each log entry is written as a separate JSON object on a new line.
    """

    def __init__(
        self,
        filename: str,
        mode: str = "a",
        encoding: Optional[str] = "utf-8"
    ) -> None:
        """
        Initialize the handler with file parameters.

        Args:
            filename: Path to the log file
            mode: File opening mode (default: append)
            encoding: File encoding
        """
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding

        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Write the log record to the file as JSON.

        Args:
            record: The log record to be processed
        """
        try:
            # Create a dictionary from the log record
            log_entry: Dict[str, Any] = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": self.format(record),
                "module": record.module,
                "line_number": record.lineno,
            }

            # Add exception info if available
            if record.exc_info:
                log_entry["exception"] = {
                    "type": record.exc_info[0].__name__,
                    "message": str(record.exc_info[1]),
                }

            # Write to file
            with open(self.filename, self.mode, encoding=self.encoding) as file:
                file.write(json.dumps(log_entry) + "\n")

        except Exception:
            self.handleError(record)