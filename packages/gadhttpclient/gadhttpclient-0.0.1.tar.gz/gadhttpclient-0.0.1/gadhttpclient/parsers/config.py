from pathlib import Path

from gadhttpclient import const
from gadhttpclient.os import HTTP
from gadhttpclient.utils import temp
from gadhttpclient.utils import urls


def getconfig(file: str) -> tuple[Path, bool]:
    if urls.checkurl(file):
        return temp.getfile(HTTP.download(file), extension=const.EXTENSION_TOML), True
    else:
        return Path(file), False
