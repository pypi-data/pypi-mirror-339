import random
from string import ascii_letters

def genInteger(min: int=1, max: int=100) -> int:
    """
    Generate a random integer between min and max.
    """
    return random.randint(min, max)

def genDecimal(min: float=2, max: float=100, precision: int = 100, scale: int = 30) -> float:
    """
    Generate a random float between min and max.
    """     
    # Generate a random float
    value = random.uniform(min, max)
    
    # Apply precision and scale
    format_str = f"{{:.{scale}f}}"
    value = float(format_str.format(value)) 
    
    # Ensure the value is within the specified range
    if len(str(value)) > (precision - scale):
        raise ValueError(f"Value {value} exceeds the specified precision of {precision} digits.")
    
    return value
    
def genString(length: int=-1, min: int = 5, max: int = 20) -> str:
    """
    Generate a random string of fixed length.
    """
    if length == -1:
        return ''.join(random.choice(ascii_letters) for _ in range(random.randint(min, max)))
    else:
        return '' if length == 0 else ''.join(random.choice(ascii_letters) for i in range(length))
    
def genBool() -> bool:
    """
    Generate a random boolean value.
    """
    return random.choice([True, False])