import abc

from fastapi import HTTPException


class BaseSQLAlchemyErrorParser(abc.ABC):
    @abc.abstractmethod
    def parse(self) -> HTTPException:
        raise NotImplementedError
