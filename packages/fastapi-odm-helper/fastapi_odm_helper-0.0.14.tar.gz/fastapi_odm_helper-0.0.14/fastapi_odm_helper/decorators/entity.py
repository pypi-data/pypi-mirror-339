import re
from typing import Callable, Type, TypeVar

T = TypeVar('T')


EXCEPTION_NAMES = {'categories'}


def underscoring_entity_name(entity_name: str):
    return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', entity_name)

def standardize_entity_name(table_name: str) -> str:
    transformed_name = underscoring_entity_name(table_name[: -len("Entity")]).lower()

    is_exception = any(name.lower() in transformed_name for name in EXCEPTION_NAMES)

    if is_exception:
        return transformed_name

    return f'{transformed_name}s'

def Entity() -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        class Settings:
            name = standardize_entity_name(cls.__name__)

        setattr(cls, "Settings", Settings)
        return cls

    return decorator
