import asyncio
import csv
import json
from pathlib import Path

import aiohttp
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


def convert_to_dict(df):
    # remove RXX: prefix from SKU (not needed)
    df['SKU'] = df['SKU'].apply(lambda x: x.split(":")[-1].split(" ")[0])
    df['TYPE'] = df['TYPE'].apply(lambda x: 'single' if x == 'S' else 'bifocal' if x == 'B' else 'unknown')
    df['SIZE'] = df['SIZE'].apply(map_size)
    df['APPEARANCE'] = df['GENDER'].apply(map_gender)
    df = df.drop(columns=['TINT', 'GENDER', 'MATERIAL'])
    df.columns = map(str.lower, df.columns)

    # with open(Path("/home/thomas/Documents/wichtig/reims/new-data/csv/sm_" + file.split(".")[0] + ".csv"), 'w', encoding='utf-8') as f:
    #     df.to_csv(f)

    final = []
    for i, col in enumerate(df.iterrows()):
        col = col[1]
        if col['sku'] == '':
            continue
        if any(c.isalpha() for c in col['sku']):
            col['sku'] = -1
        od_df = {'sphere': float(col['odsphere']), 'axis': float(col['odaxis']), 'cylinder': float(col['odcylinder'])}
        os_df = {'sphere': float(col['ossphere']), 'axis': float(col['osaxis']), 'cylinder': float(col['oscylinder'])}
        if col['type'] != 'single':
            od_df['add'] = float(col['odadd'])
            os_df['add'] = float(col['osadd'])
        location = 'sm' if int(col['sku']) > 5000 else 'sa'
        final.append({'sku': int(col['sku']), 'glassesType': col['type'], 'od': od_df, 'os': os_df,
                      'appearance': col['appearance'], 'glassesSize': col['size'], 'location': location})
    return final


def convert_to_mysql(glasses):
    sqls = []
    eye_counter = 1
    glasses_counter = 1
    dispense_counter = 1
    for glass in glasses:
        sqls.append(f"INSERT INTO eye VALUES({eye_counter}, '{glass['od']['sphere']}'," +
                    f" '{glass['od']['cylinder']}', '{glass['od']['axis']}', '{glass['od'].get('add', '')}');")
        sqls.append(f"INSERT INTO eye VALUES({eye_counter + 1}, '{glass['os']['sphere']}'," +
                    f" '{glass['os']['cylinder']}', '{glass['os']['axis']}', '{glass['os'].get('add', '')}');")
        sqls.append(f"INSERT INTO dispense VALUES ({dispense_counter},'2019-08-15 15:48:19');")
        sqls.append(f"INSERT INTO glasses VALUES ({glasses_counter}, {glass['sku']}," +
                    f" '{glass['glassesType']}', '{glass['glassesSize']}', '{glass['appearance']}', {dispense_counter}," +
                    f" '{glass['location']}', 0, {eye_counter + 1}, {eye_counter});")
        eye_counter += 2
        glasses_counter += 1
        dispense_counter += 1
        sqls.append("")
    return sqls


# p = Path('/home/thomas/Documents/wichtig/reims/new-data/SM_2020')
# files = [
#     "Dispense.dbf",
#     "Glsku.dbf",
#     "NOTFOUND.dbf"
# ]
# for file in files:
#     print("\n" + file + "\n---------------------------")
#     dbf = DBF(p / file, char_decode_errors='ignore')
#     frame = pd.DataFrame(iter(dbf))
#     print(frame)
#     dict_list = convert_to_dict(frame)


# Converting to JSON for testing in frontend
dbf_sa = DBF(Path("files/GLSKU_SA.dbf"))
dbf_sm = DBF(Path("files/GLSKU_SM.dbf"))
df_sa = pd.DataFrame(iter(dbf_sa))
df_sm = pd.DataFrame(iter(dbf_sm))
df = pd.concat([df_sa, df_sm])
final = convert_to_dict(df)

sql_queries = convert_to_mysql(final)
with open(Path("/home/thomas/projects/reims2-backend/src/main/resources/db/mysql/populateDB.sql"), 'w', encoding='utf-8') as f:
    for line in sql_queries:
        f.write(f"{line}\n")


# with open(Path("../").resolve() / "reims2-frontend/assets/out.json", 'w', encoding='utf-8') as f:
#     json.dump(final, f, ensure_ascii=False, indent=4)

# Upload URLs to backend
# async def make_parallel_post(data):
#     async with aiohttp.ClientSession() as session:
#         async with session.post("https://api.reims2.duckdns.org/pvh/api/glasses", json=data) as resp:
#             print(f"Status {resp.status} for SKU {data['sku']}")

# loop = asyncio.get_event_loop()
# tasks = []
# for item in final:
#     if (item['sku'] < 4700 or item['sku'] > 5300):
#         continue
#     task = asyncio.ensure_future(make_parallel_post(item))
#     tasks.append(task)
# loop.run_until_complete(asyncio.wait(tasks))
