"""Main module."""
from pathlib import Path

import dbfread
import pandas as pd
from dbfread import DBF

p = Path('files')
files = [
    "Glsku.dbf",
    "Dispense.dbf",
    "Rdinv.dbf",
    "Rdtrak.dbf",
    "Rdadd.dbf",
    "Readd.dbf",
    "Deleted.dbf"
]

for file in files:
    try:
        print("\n" + file + "\n---------------------------")
        dbf = DBF(p / file, load=True, char_decode_errors='ignore')
        frame = pd.DataFrame(iter(dbf))
        print(frame)
    except Exception as e:
        print(e)
