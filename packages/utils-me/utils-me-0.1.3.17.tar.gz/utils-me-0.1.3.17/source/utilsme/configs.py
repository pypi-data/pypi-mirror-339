import re

DEFAULT_SETTINGS = {
    "separator": ",",
    "header": True,
    "encoding": "utf-8",
    "decimal": ".",
    "quote_char": '"',
    "null_value": None,
    "date_format": None,
    "time_format": None,
    "datetime_format": None,
    "line_terminator": "\n",
    "escapechar": None
}

DEFAULT_DATETIME_FORMAT = {
    "datetime": "YYYY-MM-DD HH:MM:SS",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS"
}

USER_TO_PYTHON_FORMAT_MAPPING = {
    "YYYY": "%Y",
    "YY": "%y",
    "MM": "%m",
    "DD": "%d",
    "HH": "%H",
    "hh": "%I",
    "mm": "%M",
    "SS": "%S",
    "AM/PM": "%p",
}

def config_me(conf_cls):
    """
    A decorator to dynamically inject a configuration object into a class instance.

    This decorator adds an instance of the specified configuration class (`conf_cls`) 
    as an attribute (`_config`) to the decorated class. It preserves the original 
    `__init__` method of the decorated class and ensures that the configuration 
    object is initialized before the original initialization logic is executed.

    Args:
        conf_cls (type): The configuration class to be instantiated and injected 
                            into the decorated class.

    Returns:
        function: The decorated class with the `_config` attribute added.

    Example:
        class Config:
            def __init__(self):
                self.setting = "default"

        @config_me(Config)
        class MyClass:
            def __init__(self, name):
                self.name = name

        obj = MyClass("example")
        print(obj._config.setting)  # Output: "default"
    """
    def decorator(self):
        init = self.__init__

        def wrapper(self, *args, **kwargs):
            self._config = conf_cls()
            init(self, *args, **kwargs)

        self.__init__ = wrapper
        return self
    return decorator


def add_defaults_values(fn) -> dict:
    """
    A decorator to add default values to the configuration dictionary.
    """
    def wrapper(*args, **kwargs):
        
        result = fn(*args, **kwargs)
        
        if result['format'].lower() == 'csv':
            for key, value in DEFAULT_SETTINGS.items():
                if key not in result:
                    result[key] = value
            # Set default values for CSV-specific settings
        elif result['format'].lower() == 'json':
            # Add JSON-specific defaults if any
            pass
        return result
    return wrapper

def user_to_python_format(user_format: str) -> str:
    
    def replace_placeholder(match):
        placeholder = match.group(0)
        return USER_TO_PYTHON_FORMAT_MAPPING.get(placeholder, placeholder)

    # Use regex to find and replace placeholders
    pattern = re.compile("|".join(re.escape(key) for key in USER_TO_PYTHON_FORMAT_MAPPING.keys()))
    python_format = pattern.sub(replace_placeholder, user_format)
    return python_format
