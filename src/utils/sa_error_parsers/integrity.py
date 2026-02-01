"""
Convinient SQLAlchemy error parser.
"""

import re
from enum import StrEnum
from typing import Callable

from sqlalchemy.exc import IntegrityError

from utils.sa_error_parsers.base import BaseSQLAlchemyErrorParser


class IntegrityErrorSubtype(StrEnum):
    UNIQUE = "unique"
    NOT_NULL = "not_null"
    CHECK = "check"
    FOREIGN_KEY = "foreign_key"
    UNKNOWN = "unknown"


class SQLAlchemyIntegrityErrorParser(BaseSQLAlchemyErrorParser):
    def __init__(self, exc: IntegrityError) -> None:
        self.exc = exc
        self.message = exc.orig.args[0] if exc.orig and exc.orig.args else ""
        self.default_error_message = "Database integrity error"

    def parse(self) -> str:
        subtype = self._define_subtype()

        return self._handlers.get(subtype, self._handle_unknown_violation)() or self.default_error_message

    def _define_subtype(self) -> IntegrityErrorSubtype:
        msg = self.message.casefold()

        if "unique constraint" in msg or "duplicate key value" in msg:
            return IntegrityErrorSubtype.UNIQUE
        if "null value in column" in msg:
            return IntegrityErrorSubtype.NOT_NULL
        if "check constraint" in msg:
            return IntegrityErrorSubtype.CHECK
        if "foreign key constraint" in msg:
            return IntegrityErrorSubtype.FOREIGN_KEY

        return IntegrityErrorSubtype.UNKNOWN

    def _handle_unique_violation(self) -> str | None:
        match = re.search(r"Key \((.+?)\)=\(.+?\) already exists", self.message)

        if match:
            field: str = match.group(1).split(".")[-1]

            return f"{field.capitalize().replace('_', ' ')} already exists"

        return None

    def _handle_not_null_violation(self) -> str | None:
        match = re.search(r'null value in column "(.+?)"', self.message)

        if match:
            field = match.group(1)

            return f"{field.capitalize().replace('_', ' ')} is required"

        return None

    def _handle_check_violation(self) -> str | None:
        match = re.search(r'check constraint "(.+?)"', self.message)

        if match:
            constraint = match.group(1)

            return f"Constraint failed: {constraint}"

        return None

    def _handle_foreign_key_violation(self) -> str:
        match = re.search(r'is not present in table "(.+?)"', self.message)

        if match:
            table = match.group(1)

            return f"Related {table.replace('_', ' ')} not found"

        return "Related data is not found"

    def _handle_unknown_violation(self) -> str:
        return self.default_error_message

    @property
    def _handlers(self) -> dict[IntegrityErrorSubtype, Callable[[], str | None]]:
        return {
            IntegrityErrorSubtype.UNIQUE: self._handle_unique_violation,
            IntegrityErrorSubtype.NOT_NULL: self._handle_not_null_violation,
            IntegrityErrorSubtype.CHECK: self._handle_check_violation,
            IntegrityErrorSubtype.FOREIGN_KEY: self._handle_foreign_key_violation,
            IntegrityErrorSubtype.UNKNOWN: self._handle_unknown_violation,
        }
