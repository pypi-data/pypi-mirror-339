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
    last_part = base_name.split('_')[-1]

    is_exception = any(last_part in name for name in PLURAL_NAME_MAP.keys())
    print('is_exception', is_exception)
    if is_exception:
        parts = base_name.rsplit('_', 1)
        first_parts = parts[0] if len(parts) > 1 else ''
        print(f'{first_parts}_{PLURAL_NAME_MAP[last_part]}')
        return f'{first_parts}_{PLURAL_NAME_MAP[last_part]}'

    return f'{base_name}s'


def Entity() -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        class Settings:
            name = standardize_entity_name(cls.__name__)

        setattr(cls, "Settings", Settings)
        return cls

    return decorator
