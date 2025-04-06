import time
from contextvars import Token
from typing import Callable, Optional, Type

from . import main


def invoke_with_backoff(
    f: Callable,
    request_items: dict,
    unprocessed_key: str,
    max_attempts: int = 5,
):
    responses = []
    backoff_sleep = 0.05
    attempts = 0

    unprocessed_items = request_items
    while unprocessed_items:
        response = f(RequestItems=unprocessed_items)
        responses.append(response)

        unprocessed_items = response[unprocessed_key]

        if unprocessed_items:  # pragma: no cover
            attempts += 1
            if attempts > max_attempts:
                raise Exception(f"Exceeded max attempts ({max_attempts}) to process unprocessed keys")

            time.sleep(backoff_sleep)
            backoff_sleep *= 2

    return responses


class BatchWriter:
    def __init__(self, table: Type["main.Dyntastic"], batch_size: int = 25):
        self.table = table
        self.batch_size = batch_size
        self.batch: list = []
        self.batches_submitted = 0
        self._context_var_reset_token: Optional[Token] = None

    def __enter__(self):
        self._context_var_reset_token = self.table._dyntastic_batch_writer.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        assert self._context_var_reset_token is not None
        self.table._dyntastic_batch_writer.reset(self._context_var_reset_token)
        self._context_var_reset_token = None

        if not exc_type:
            self._commit()

    def _commit(self):
        if self.batch:
            self.table.submit_batch_write(self.batch)
            self.batch = []
            self.batches_submitted += 1

    def add(self, item):
        self.batch.append(item)
        if len(self.batch) >= self.batch_size:
            self._commit()
