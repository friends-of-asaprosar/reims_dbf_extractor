"""Main module."""
from pathlib import Path

import json
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
        dbf = DBF(p / file, char_decode_errors='ignore')
        frame = pd.DataFrame(iter(dbf))
        print(frame)
    except Exception as e:
        print(e)

# Converting to JSON for testing in frontend
dbf_main = DBF(p / "Glsku.dbf")
df = pd.DataFrame(iter(dbf_main))
# drop unused columns
df = df.drop(columns=['TINT', 'ENTERDATE'])
# remove RXX: prefix from SKU (not needed)
df['SKU'] = df['SKU'].apply(lambda x: x.split(":")[-1])

# convert to JSON and directly save in frontend assets foldeer
dfj = json.loads(df.reset_index().to_json(orient='records'))
with open(Path("../").resolve() / "reims2-frontend/assets/out.json", 'w', encoding='utf-8') as f:
    json.dump(dfj, f, ensure_ascii=False, indent=4)
