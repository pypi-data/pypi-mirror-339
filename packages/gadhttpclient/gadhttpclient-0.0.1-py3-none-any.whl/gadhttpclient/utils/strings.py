import re

import tomli

from gadhttpclient import const


def separate(value: str) -> list[str]:
    return re.split(const.REGEXP_SEPARATOR_PATTERN, value)


def concat(words: list[str], symbol: str) -> str:
    return symbol.join(words)


def to_snake(value: str) -> str:
    return concat(separate(value), symbol=const.SYMBOL_LOWER_HYPHEN).lower()


def to_pascal(string: str) -> str:
    if not (words := re.split(const.REGEXP_NON_ALPHANUMERIC, string)):
        return string

    new = []

    for word in words:
        if not word:
            continue
        if word.isupper():
            new.append(word)
        else:
            new.append(word[0].upper() + word[1:])

    return concat(new, const.SYMBOL_EMPTY)


def to_toml(content: str) -> dict:
    return tomli.loads(content)


def sortimports(lines: list[str]) -> str:
    imports, code = [], []
    for line in lines:
        (imports if re.match(const.REGEXP_IMPORT_PATTERN, line) else code).append(line)
    return "".join(sorted(imports) + code)
