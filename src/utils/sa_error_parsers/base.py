import abc


class BaseSQLAlchemyErrorParser(abc.ABC):
    @abc.abstractmethod
    def parse(self) -> str:
        raise NotImplementedError
