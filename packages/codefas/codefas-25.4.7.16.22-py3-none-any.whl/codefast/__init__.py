import ast
import codefast.reader
import codefast.utils as utils
from codefast.base.format_print import FormatPrint as fp
from codefast.constants import constants
from codefast.ds import fpjson, fplist, nstr, pair_sample, fpdict, flatten
from codefast.functools.random import random_string, sample, sample_one, hex
from codefast.io import FastJson
from codefast.io import FileIO as io
from codefast.io import dblite
from codefast.io.osdb import osdb
from codefast.io.fdb import fdb
from codefast.io._json import fpjson
from codefast.logger import error, info, warning
from codefast.utils import (b64decode, b64encode, cipher, decipher, retry,
                            shell, syscall, uuid, md5sum)
from codefast.os import getenv
from codefast.models.date import realdate, arealdate
from codefast.asyncio.logger import alogger


def islist(x) -> bool:
    return isinstance(x, list)

# ---------------------------- Math methods


def round4(number: float) -> float:
    return round(number, 4)


def round2(number: float) -> float:
    return round(number, 2)

# ---------------------------- pandas read files


def csv(csv_file):
    import pandas as pd
    return pd.read_csv(csv_file)


def excel(excel_file):
    import pandas as pd
    return pd.read_excel(excel_file)


def date_file(prefix: str, file_ext: str) -> str:
    import datetime
    return f"{prefix}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.{file_ext}"


def eval(s: str):
    try:
        import json
        return json.loads(s)
    except json.decoder.JSONDecodeError as e:
        warning(e)
        return ast.literal_eval(s)


def generate_version():
    """ Generate package version based on date
    """
    import datetime
    return datetime.datetime.now().strftime('%y.%m.%d.%H')


def blocking():
    # block main thread from exiting
    import time
    while True:
        time.sleep(1 << 10)


dic = fpdict
js = FastJson()
lis = fplist
read = io.read
