import json
from ast import literal_eval
from collections.abc import Callable
from datetime import date
from logging import FileHandler, LogRecord, StreamHandler
from typing import TypeAlias

from azure.core.credentials import (
    AzureNamedKeyCredential,
    AzureSasCredential,
    TokenCredential,
)
from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableClient
from azure.identity import DefaultAzureCredential

from ..utils import create_id
from .base_handler import BaseHandler

TableCredential: TypeAlias = (
    AzureSasCredential
    | AzureNamedKeyCredential
    | TokenCredential
    | DefaultAzureCredential
    | None
)


class DatalakeTableHandler(BaseHandler):
    def __init__(
        self,
        storage_account_name: str,
        table_name: str,
        credential: TableCredential | None = None,
        /,
        part_key: str = None,
        row_key_fn: Callable = None,
        to_stream: bool = True,
        stream_handler_config: dict = None,
        to_file: bool = True,
        file_handler_config: dict = None,
    ):
        self.account_name = storage_account_name
        self.endpoint = f"https://{self.account_name}.table.core.windows.net"
        self.table_name = table_name
        self.credential = credential or DefaultAzureCredential()
        self.part_key = part_key or str(date.today())
        self.row_key_fn: Callable = self.set_row_key_fn(row_key_fn)
        self.table = self._setup_table()
        self.stream = self._setup_stream_handler(stream_handler_config)
        self.to_stream = to_stream
        self.file = self._setup_file_handler(file_handler_config)
        self.to_file = to_file
        self.filters = []
        self.lock = None

    def emit(self, record: LogRecord) -> str:
        """
        Emit a log record.

        This method formats the log record, sends it to the configured stream
        and file handlers, and creates an entity in the Azure Table Storage.

        Args:
            record: LogRecord object containing the log information

        Returns:
            str: The formatted log message
        """
        record_dict = {
            "level_number": record.levelno,
            "level_name": record.levelname.lower(),
            "module": record.module,
            "line_number": record.lineno,
            "function_name": record.funcName,
            "message": record.getMessage(),
            # "created": str(record.created),
            # "asctime": str(self.formatter.formatTime(record)),
            # "msecs": str(record.msecs),
            # "name": str(record.name),
            # "pathname": str(record.pathname),
            # "filename": str(record.filename),
            # "relativeCreated": str(record.relativeCreated),
            # "thread": str(record.thread),
            # "threadName": str(record.threadName),
            # "process": str(record.process),
        }
        if self.to_stream:
            self.stream.setFormatter(self.formatter)
            self.stream.emit(record)
        if self.to_file:
            self.file.setFormatter(self.formatter)
            self.file.emit(record)
        entity = self._create_table_entity(record_dict)
        self.table.create_entity(entity)

    def _setup_table(self) -> TableClient:
        """
        Initialize and create an Azure Table Storage table if it doesn't exist.

        Creates a connection to the table specified in the handler configuration.
        If the table doesn't exist, it will be created. If it already exists,
        the function will silently continue using the existing table.

        Returns:
            TableClient: Initialized Azure Table Storage client
        """
        table = TableClient(
            self.endpoint,
            self.table_name,
            credential=self.credential,
        )
        try:
            table.create_table()
        except ResourceExistsError:
            pass
        return table

    def set_row_key_fn(self, fn: Callable = None) -> Callable:
        """
        Set the function used to generate row keys for table entities.

        Args:
            fn: Custom function to generate row keys. If None or not callable,
                defaults to the create_id function.

        Returns:
            Callable: The function that will be used to generate row keys
        """
        return fn if isinstance(fn, Callable) else create_id

    def _setup_stream_handler(self, config: dict = None) -> StreamHandler:
        """
        Initialize a StreamHandler for console logging.

        Args:
            config: Dictionary containing configuration options for the
                   StreamHandler. If None, default configuration is used.

        Returns:
            StreamHandler: Configured handler for console output
        """
        return StreamHandler(**(config or {}))

    def _setup_file_handler(self, config: dict = None) -> FileHandler:
        """
        Initialize a FileHandler for file-based logging.

        Args:
            config: Dictionary containing configuration options for the
                   FileHandler. If None, defaults to using 'app.log' as filename.

        Returns:
            FileHandler: Configured handler for file output
        """
        config = {"filename": "app.log", **(config or {})}
        return FileHandler(**config)

    def _create_table_entity(self, data: dict) -> dict:
        """
        Create an entity for Azure Table Storage from log record data.

        This method transforms log data into the format required for Azure Table
        Storage, extracting the message field for special processing and adding
        required partition and row keys.

        Args:
            data: Dictionary containing log record data

        Returns:
            Dictionary formatted as an Azure Table Storage entity
        """
        message = data.pop("message")
        return {
            "PartitionKey": self.part_key,
            "RowKey": create_id(),
            **data,
            "message": json.dumps(literal_eval(message)),
        }
