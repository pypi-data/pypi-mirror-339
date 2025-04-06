import logging
import threading
from typing import List, Optional


class BatchedHandler(logging.Handler):
    """
    Handler that collects log records in batches and processes them periodically.

    This is useful for reducing I/O operations or network calls when
    logging large volumes of messages.
    """

    def __init__(
        self,
        batch_size: int = 100,
        flush_interval: float = 5.0,
        target_handler: Optional[logging.Handler] = None
    ) -> None:
        """
        Initialize the batched handler.

        Args:
            batch_size: Maximum records to collect before flushing
            flush_interval: Maximum seconds between flushes
            target_handler: Optional handler to receive the batched records
        """
        super().__init__()
        self.batch_size = max(1, batch_size)
        self.flush_interval = max(0.1, flush_interval)
        self.target_handler = target_handler

        self._buffer: List[logging.LogRecord] = []
        self._lock = threading.RLock()
        self._timer: Optional[threading.Timer] = None
        self._start_timer()

    def _start_timer(self) -> None:
        """Start the timer for periodic flushing."""
        self._timer = threading.Timer(self.flush_interval, self._timed_flush)
        self._timer.daemon = True
        self._timer.start()

    def _timed_flush(self) -> None:
        """Flush the buffer based on timer and restart the timer."""
        self.flush()
        self._start_timer()

    def emit(self, record: logging.LogRecord) -> None:
        """
        Add the record to the buffer and flush if batch_size is reached.

        Args:
            record: Log record to process
        """
        try:
            with self._lock:
                self._buffer.append(record)

                if len(self._buffer) >= self.batch_size:
                    self.flush()
        except Exception:
            self.handleError(record)

    def flush(self) -> None:
        """Process all records in the buffer."""
        with self._lock:
            if not self._buffer:
                return

            # Process the batch
            try:
                self._process_batch(list(self._buffer))
            finally:
                self._buffer.clear()

    def _process_batch(self, records: List[logging.LogRecord]) -> None:
        """
        Process a batch of records.

        Args:
            records: List of records to process
        """
        # Use target handler if provided
        if self.target_handler:
            for record in records:
                self.target_handler.handle(record)
        else:
            # Default implementation can be overridden in subclasses
            for record in records:
                message = self.format(record)
                print(f"Batched log: {message}")

    def close(self) -> None:
        """Stop the timer and flush remaining records."""
        if self._timer:
            self._timer.cancel()

        self.flush()
        super().close()