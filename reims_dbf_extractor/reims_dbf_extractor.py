"""Main module."""
import dbfread

from dbfread import DBF
for record in DBF('files/DISPENSE.DBF'):
    print(record)
