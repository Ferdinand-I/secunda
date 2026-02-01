from sqlalchemy.orm import DeclarativeBase, relationships

from storage.database.settings import metadata


class Base(DeclarativeBase):
    metadata = metadata

    def __repr__(self) -> str:
        attrs = {
            key: getattr(self, key)
            for key in self.__mapper__.columns.keys()
            if not isinstance(getattr(self.__class__, key), relationships.RelationshipProperty)
        }

        attr_str = ", ".join(f"{key}={value!r}" for key, value in attrs.items())

        return f"{self.__class__.__name__}({attr_str})>"
