import datetime
import sqlite3
import xml.parsers.expat
from dataclasses import dataclass
from zipfile import ZipFile
from common import utils
import pprint as pp

# contains the actual parents
parent_elem = list()

# contains the tree statistic
xml_tree = dict()

counter = 0

p = xml.parsers.expat.ParserCreate()


class StopException(Exception):
    pass


@dataclass
class OP:
    OPName:str = ''
    UniqueOPID:str = ''
    OPTafTapCode:str = ''
    OPType:str = ''
    OPTypeGaugeChangeover:str = ''
    OPGeographicLocation:str = ''
    OPRailwayLocation:str = ''


plc_list = list()
focus_lc: OP = False
focus_lc_elem = None


def monitor_parser():
    global counter
    counter += 1
    # if counter > 1000:
    #    raise StopException()
    if (counter % 10000) == 0:
        print('.', end='')


# 3 handler functions
def start_element(name, attrs):
    global focus_lc, focus_lc_elem, plc_list
    parent_elem.append(name)
    p_str = '/'.join(parent_elem)
    monitor_parser()
    if focus_lc:
        focus_plc_elem = name
    elif name == "Primary_Location":
        focus_plc = PLC()
        plc_list.append(focus_plc)


def end_element(name):
    global focus_lc
    parent_elem.pop()
    if name == "Primary_Location":
        focus_plc = False


def char_data(data: str):
    global focus_lc, focus_lc_elem
    if len(data.strip()) > 0:
        if focus_lc:
            setattr(focus_lc, focus_lc_elem, data)


p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

print('\n-------')
# open the zipfile and parse the xml
zfile_name = "data/AT RINF Data_2021-3Q_UpdateOn2021-08-10.zip"
file_name = "AT RINF Data_2021-3Q_UpdateOn2021-08-10.xml"
print(f'read file {file_name}')
with ZipFile(zfile_name, "r") as zfile:
    with zfile.open(file_name, "r") as file:
        try:
            p.ParseFile(file)
        except StopException as e:
            print('OK ;-)')

print('-------\nprepare data records')

sql_records = list()
plc_keys = list()
for plc in plc_list:
    sql_records.append(plc.__dict__)
plc_list = list()

print('\n-------\nwrite data records')

today = datetime.datetime.now().date()
counter = 0
with sqlite3.connect("../common/data/open-railway.sqlite",
                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("delete from 'rinf.op'")
    cursor.executemany('INSERT INTO "rinf.op" '
                       '() '
                       'VALUES'
                       '(:)'
                       , sql_records)
    conn.commit()

print(f"PLC: {len(sql_records)} data records were written")