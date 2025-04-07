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