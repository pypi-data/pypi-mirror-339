from pydantic import BaseModel, ConfigDict
from typing import Protocol, Union, TypeVar

from pydantic.v1.typing import get_origin, get_args

from fellow.clients.OpenAIClient import OpenAIClient


class CommandContext(BaseModel):
    ai_client: OpenAIClient

    model_config = ConfigDict(arbitrary_types_allowed=True)

class CommandInput(BaseModel):
    @classmethod
    def command_schema(cls) -> dict:
        fields = {}
        for name, field in cls.model_fields.items():
            field_type = field.annotation
            is_optional = False

            # Check for Optional[...] type
            origin = get_origin(field_type)
            args = get_args(field_type)
            if origin is Union and type(None) in args:
                field_type = [a for a in args if a is not type(None)][0]
                is_optional = True

            # Only mark as optional if either type is Optional[...] or it's not required
            is_optional = is_optional or not field.is_required()

            type_name = getattr(field_type, '__name__', str(field_type))
            type_str = f"{type_name}{' (optional)' if is_optional else ''}"

            description = field.description or ""
            fields[name] = f"{type_str} - {description}"
        return fields


T = TypeVar("T", bound=CommandInput)


class CommandHandler(Protocol[T]):
    def __call__(self, args: T, context: CommandContext) -> str:
        ...
