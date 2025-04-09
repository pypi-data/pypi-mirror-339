from typing import Any
from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class Color(BaseModel):
    id: str
    r: int
    g: int
    b: int

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, Color) and
                self.id == other.id and
                self.r == other.r and
                self.g == other.g and
                self.b == other.b)

    def __hash__(self) -> int:
        return hash((self.id, self.r, self.g, self.b))


class Font(BaseModel):
    id: str
    name: str
    size: int

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, Font) and
                self.id == other.id and
                self.size == other.size and
                self.name == other.name)

    def __hash__(self) -> int:
        return hash((self.id, self.size, self.name))


class Mark(BaseModel):
    category: Literal['bold', 'italic', 'superscripted', 'serifed', 'monospaced', 'textStyle', 'link']

    @model_validator(mode='before')
    def check_details(self: Any) -> Any:
        mark_type = self.get('category')

        if mark_type == 'textStyle':
            if 'color' not in self and 'font' not in self:
                raise ValueError('color or font must be provided when type is textStyle')
            if 'url' in self:
                raise ValueError('url should not be provided when type is textStyle')

        elif mark_type == 'link':
            if 'url' not in self:
                raise ValueError('url must be provided when type is link')
            if 'textStyle' in self:
                raise ValueError('textStyle should not be provided when type is link')
        return self

    def __eq__(self, other):
        return isinstance(other, Mark) and self.category == other.category

    def __hash__(self) -> int:
        return hash(self.category)


class TextStyleMark(Mark):
    color: Optional[Color] = None
    font: Optional[Font] = None

    def __eq__(self, other):
        return (isinstance(other, TextStyleMark) and
                self.category == other.category and
                self.color == other.color and
                self.font == other.font)

    def __hash__(self) -> int:
        return hash((self.category, self.color, self.font))


class UrlMark(Mark):
    url: str

    def __eq__(self, other):
        return (isinstance(other, UrlMark) and
                self.category == other.category and
                self.url == other.url)

    def __hash__(self) -> int:
        return hash((self.category, self.url))
