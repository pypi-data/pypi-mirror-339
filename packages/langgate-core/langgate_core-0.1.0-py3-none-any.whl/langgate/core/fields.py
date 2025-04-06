from typing import Annotated

from pydantic import (
    AfterValidator,
    AnyHttpUrl,
    PlainValidator,
    TypeAdapter,
)

AnyHttpUrlAdapter = TypeAdapter(AnyHttpUrl)

# https://github.com/pydantic/pydantic/issues/7186
HttpUrlStr = Annotated[
    str,
    PlainValidator(lambda x: AnyHttpUrlAdapter.validate_strings(x)),
    AfterValidator(lambda x: str(x).rstrip("/")),
]
