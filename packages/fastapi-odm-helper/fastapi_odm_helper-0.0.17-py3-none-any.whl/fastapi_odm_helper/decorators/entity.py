import re
from typing import Callable, Type, TypeVar

T = TypeVar('T')


PLURAL_NAME_MAP = {
    'category': 'categories',
}


def underscoring_entity_name(entity_name: str):
    return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', entity_name)

def standardize_entity_name(table_name: str) -> str:
    base_name = underscoring_entity_name(table_name[: -len("Entity")]).lower()
    last_name = base_name.split('_')[-1]

    is_plural_name = any(name.lower() in last_name for name in PLURAL_NAME_MAP.keys())
    if is_plural_name:
        return PLURAL_NAME_MAP[last_name]

    return f'{base_name}s'


def Entity() -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        class Settings:
            name = standardize_entity_name(cls.__name__)

        setattr(cls, "Settings", Settings)
        return cls

    return decorator
