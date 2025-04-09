import re
from typing import Callable, Type, TypeVar

T = TypeVar('T')


EXCEPTION_NAMES = {'Categories'}


def underscoring_entity_name(entity_name: str):
    return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', entity_name)

def standardize_entity_name(table_name: str, not_convert_name: bool = False) -> str:
    table_name = underscoring_entity_name(table_name[: -len("Entity")]).lower()

    if not_convert_name or table_name in EXCEPTION_NAMES:
        return table_name

    return f'{table_name}s'

def Entity(not_convert_name: bool = False) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        class Settings:
            name = standardize_entity_name(cls.__name__, not_convert_name=not_convert_name)

        setattr(cls, "Settings", Settings)
        return cls

    return decorator
