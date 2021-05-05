"""Main module."""
from pathlib import Path

import json
import pandas as pd
from dbfread import DBF


def map_size(x):
    if x == 'S':
        return 'small'
    if x == 'C':
        return 'child'
    if x == 'L':
        return 'large'
    if x == 'M':
        return 'medium'
    return 'unknown'


def map_gender(x):
    if x == 'M':
        return 'masculine'
    if x == 'F':
        return 'feminine'
    if x == 'U':
        return 'neutral'
    return 'unknown'


p = Path('files')
files = [
    "Glsku.dbf",
    # "Dispense.dbf",
    # "Rdinv.dbf",
    # "Rdtrak.dbf",
    # "Rdadd.dbf",
    # "Readd.dbf",
    # "Deleted.dbf"
]
for file in files:
    try:
        print("\n" + file + "\n---------------------------")
        dbf = DBF(p / file, char_decode_errors='ignore')
        frame = pd.DataFrame(iter(dbf))
        print(frame)
    except Exception as e:
        print(e)

# Converting to JSON for testing in frontend
dbf_main = DBF(p / "Glsku_old.dbf")
df = pd.DataFrame(iter(dbf_main))

# remove RXX: prefix from SKU (not needed)
df['SKU'] = df['SKU'].apply(lambda x: x.split(":")[-1])
df['TYPE'] = df['TYPE'].apply(lambda x: 'single' if x == 'S' else 'bifocal' if x == 'B' else 'unknown')
df['SIZE'] = df['SIZE'].apply(map_size)
df['APPEARANCE'] = df['GENDER'].apply(map_gender)
df['MATERIAL'] = df['MATERIAL'].apply(lambda x: 'plastic' if x == 'P' else 'metal' if x == 'M' else 'unknown')

# drop unused columns
df = df.drop(columns=['TINT', 'ENTERDATE', 'GENDER'])

# convert to JSON and directly save in frontend assets foldeer
dfj = json.loads(df.reset_index().to_json(orient='records'))
with open(Path("../").resolve() / "reims2-frontend/assets/out.json", 'w', encoding='utf-8') as f:
    json.dump(dfj, f, ensure_ascii=False, indent=4)
