from pydantic import BaseModel, ValidationError, Field, field_validator
from typing import List, Any, Optional
import re


class ColumnModel(BaseModel):
    name: str
    type: str
    length: Optional[int] = None
    min: Optional[int] = None
    max: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str):
        """
        Validate the type of the column.
        """
        if value.startswith("decimal("):
            match = re.match(r"decimal\((\d+),(\d+)\)", value)
            if not match:
                raise ValueError("Invalid decimal type format. Use decimal(precision, scale).")
            precision, scale = map(int, match.groups())
            if precision <= 0 or scale < 0 or scale > precision:
                raise ValueError(f"Invalid precision ({precision}) or scale ({scale}) for decimal type.")
            
            cls.precision = precision
            cls.scale = scale
        return value
    
class CsvDataModel(BaseModel):
    columns: List[ColumnModel]
    name: str
    format: str
    encoding: Optional[str] = Field(
        default="utf-8",
        description="Encoding of the file"
    )
    separator: Optional[str] = Field(
        default=",",
        description="Separator used in the file"
    )
    header: Optional[bool] = Field(
        default=True,
        description="Whether the file has a header"
    )
    decimal: Optional[str] = Field(
        default=".",
        description="Decimal symbol used in the file"
    )
    quote_char: Optional[str] = Field(
        default='"',
        description="Quote character used in the file"
    )
    null_value: Optional[str] = Field(
        default=None,
        description="String representation of null values"
    )
    date_format: Optional[str] = Field(
        default=None,
        description="Date format used in the file"
    )
    time_format: Optional[str] = Field(
        default=None,
        description="Time format used in the file"
    )
    datetime_format: Optional[str] = Field(
        default=None,
        description="Datetime format used in the file"
    )
    line_terminator: str = Field(
        default="\n",
        description="Line terminator used in the file"
    )
    escapechar: Optional[str] = Field(
        default=None,
        description="Escape character used in the file"
    )
