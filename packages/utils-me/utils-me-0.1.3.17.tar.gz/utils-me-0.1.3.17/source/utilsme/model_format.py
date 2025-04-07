from pydantic import BaseModel, ValidationError, Field, field_validator
from typing import List, Any, Optional
from utilsme import DEFAULT_DATETIME_FORMAT
import re
from utilsme import user_to_python_format


class ColumnModel(BaseModel):
    name: str
    type: str
    length: Optional[int] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min: Optional[int] = None
    max: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    format: Optional[str] = None
    
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
        elif value in ["datetime", "date", "time"]:
            if not cls.format:
                cls.format = DEFAULT_DATETIME_FORMAT.get(value, None)
                
            cls.format = user_to_python_format(cls.format)
            
        return value
    
class CsvDataModel(BaseModel):
    columns: List[ColumnModel]
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
