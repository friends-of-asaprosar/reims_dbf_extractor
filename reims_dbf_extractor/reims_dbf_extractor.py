"""Main module."""
from pathlib import Path

import dbfread
import pandas as pd
from dbfread import DBF

p = Path('files')
for path in p.glob('*.DBF'):
    print(path)
    try:
        dbf = DBF(path, load=True, char_decode_errors='ignore')
        frame = pd.DataFrame(iter(dbf))
        print(frame)
    except Exception as e:
        print(e)
