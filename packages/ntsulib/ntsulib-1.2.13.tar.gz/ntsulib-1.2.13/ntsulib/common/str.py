import re

__all__ = ["n_str"]

class n_str:
    def __init__(self, arg: object = ""):
        self._string = str(arg) if arg is not None else ""

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, value: object):
        self._string = str(value) if value is not None else ""

    def setString(self, value: object):
        self._string = str(value) if value is not None else ""

    def getString(self, value: object):
        return self._string

    def to_str(self) -> str:
        return self._string

    def end_with(self, var: str) -> bool:
        return self._string.endswith(var)

    def start_with(self, var: str) -> bool:
        return self._string.startswith(var)

    def replaceAll(self, bereplaced: str, replace: str) -> 'n_str':
        return n_str(self._string.replace(bereplaced, replace))

    def replaceFirst(self, pattern, replacement) -> 'n_str':
        return n_str(re.sub(pattern, replacement, self._string, count=1))

    def replaceEnd(self, pattern, replacement) -> 'n_str':
        return n_str(re.sub(pattern + '$', replacement, self._string))

    def replaceAt(self, index: int, bereplaced: str, replace: str) -> 'n_str':
        pattern = re.escape(bereplaced)
        count = 0

        def replace_match(match):
            nonlocal count
            count += 1
            if count == index:
                return replace
            else:
                return match.group()

        return n_str(re.sub(pattern, replace_match, self._string, count=index))

    def has_digits(self) -> bool:
        return any(char.isdigit() for char in self._string)

    def count_str(self, c: str) -> int:
        return self._string.count(c)

    def split(self, delimiter: str = None, limit: int = -1) -> list:
        if delimiter is None:
            return self._string.split()
        if limit == -1:
            return self._string.split(delimiter)
        return self._string.split(delimiter, limit)

    def contains(self, s: str) -> bool:
        return s in self._string

    def index_of(self, s: str, start: int = 0) -> int:
        return self._string.find(s, start)

    def last_index_of(self, s: str, start: int = 0) -> int:
        return self._string.rfind(s, start)

    def matches(self, regex: str) -> bool:
        return re.fullmatch(regex, self._string) is not None

    def substring(self, begin: int, end: int = None) -> 'n_str':
        if end is None:
            return n_str(self._string[begin:])
        return n_str(self._string[begin:end])

    def to_lower_case(self) -> 'n_str':
        return n_str(self._string.lower())

    def to_upper_case(self) -> 'n_str':
        return n_str(self._string.upper())

    def trim(self) -> 'n_str':
        return n_str(self._string.strip())

    def concat(self, s: str) -> 'n_str':
        return n_str(self._string + str(s))

    def char_at(self, index: int) -> str:
        return self._string[index]

    def code_point_at(self, index: int) -> int:
        return ord(self._string[index])

    def is_empty(self) -> bool:
        return len(self._string) == 0

    def is_blank(self) -> bool:
        return len(self._string.strip()) == 0

    def format(self, *args, **kwargs) -> 'n_str':
        return n_str(self._string.format(*args, **kwargs))

    def join(self, iterable) -> 'n_str':
        return n_str(self._string.join(str(item) for item in iterable))

    def __len__(self):
        return len(self._string)

    def __str__(self):
        return self._string

    def __repr__(self):
        return f"n_str('{self._string}')"

    def __add__(self, other):
        if isinstance(other, (str, n_str)):
            return n_str(self._string + str(other))
        raise TypeError(f'Cannot add {type(self)} and {type(other)}')

    def __radd__(self, other):
        if isinstance(other, (str, n_str)):
            return n_str(str(other) + self._string)
        raise TypeError(f'Cannot add {type(other)} and {type(self)}')

    def __eq__(self, other):
        if isinstance(other, n_str):
            return self._string == other._string
        elif isinstance(other, str):
            return self._string == other
        else:
            return False

    def __contains__(self, item):
        return item in self._string

    def __getitem__(self, index):
        return self._string[index]
