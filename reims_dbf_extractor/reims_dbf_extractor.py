"""Main module."""
from pathlib import Path

import json
import pandas as pd
from dbfread import DBF
import asyncio
import aiohttp


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
dbf_sa = DBF(p / "GLSKU_SA.dbf")
dbf_sm = DBF(p / "GLSKU_SM.dbf")
df_sa = pd.DataFrame(iter(dbf_sa))
df_sm = pd.DataFrame(iter(dbf_sm))
df = pd.concat([df_sa, df_sm])

# remove RXX: prefix from SKU (not needed)
df['SKU'] = df['SKU'].apply(lambda x: x.split(":")[-1].split(" ")[0])
df['TYPE'] = df['TYPE'].apply(lambda x: 'single' if x == 'S' else 'bifocal' if x == 'B' else 'unknown')
df['SIZE'] = df['SIZE'].apply(map_size)
df['APPEARANCE'] = df['GENDER'].apply(map_gender)
df.columns = map(str.lower, df.columns)


final = []
# drop unused columns
for i, col in enumerate(df.iterrows()):
    col = col[1]
    od_df = {'sphere': col['odsphere'], 'axis': col['odaxis'], 'cylinder': col['odcylinder']}
    os_df = {'sphere': col['ossphere'], 'axis': col['osaxis'], 'cylinder': col['oscylinder']}
    if col['type'] != 'single':
        od_df['add'] = col['odadd']
        os_df['add'] = col['osadd']
    location = 'sm' if int(col['sku']) > 5000 else 'sa'
    final.append({'id': i, 'sku': col['sku'], 'glassesType': col['type'], 'od': od_df, 'os': os_df,
                  'appearance': col['appearance'], 'glassesSize': col['size'], 'dispense': {}, 'material': 'any', 'location': location})


# with open(Path("../").resolve() / "reims2-frontend/assets/out.json", 'w', encoding='utf-8') as f:
#    json.dump(final, f, ensure_ascii=False, indent=4)


# Upload URLs to backend

async def make_parallel_post(data, i):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.reims2.duckdns.org/pvh/api/glasses", json=data) as resp:
            print(resp.status, i)

loop = asyncio.get_event_loop()
tasks = []
for i, item in enumerate(final):
    if (i < 5000 or i > 7000):
        continue
    task = asyncio.ensure_future(make_parallel_post(item, i))
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))
