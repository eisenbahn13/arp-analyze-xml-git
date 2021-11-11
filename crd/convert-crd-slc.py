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
class SLC:
    Country_ISO_Code: str = ''
    Responsible_IM_Code: str = ''
    Subsidiary_Location_Code: str = ''
    Location_Code: str = ''
    Subsidiary_Type_Code: str = ''
    Subsidiary_Location_Name: str = ''
    Start_Validity: str = ''
    AllocationCompany: str = ''
    Active_Flag: bool = False
    Add_Date: str = ''
    Modified_Date: str = ''
    End_Validity: str = ''
    Free_Text: str = ''
    Latitude: float = 0.0
    Longitude: float = 0.0


plc_list = list()
focus_lc: SLC = False
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
        focus_lc_elem = name
    elif name == "Subsidiary_Location":
        focus_lc = SLC()
        plc_list.append(focus_lc)


def end_element(name):
    global focus_lc
    parent_elem.pop()
    if name == "Subsidiary_Location":
        focus_lc = False


def char_data(data: str):
    global focus_lc, focus_lc_elem
    if len(data.strip()) > 0:
        if focus_lc and focus_lc_elem:
            setattr(focus_lc, focus_lc_elem, data)


p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

print('\n-------')
# open the zipfile and parse the xml
zfile_name = "data/SubsidiaryLocation v20210812.xml.zip"
file_name = "SubsidiaryLocation v20210812.xml"
print(f'read file {file_name}')
with ZipFile(zfile_name, "r") as zfile:
    with zfile.open(file_name, "r") as file:
        try:
            p.ParseFile(file)
        except StopException as e:
            print('OK ;-)')

print('\n-------\nprepare data records')

slc_insert = list()
plc_keys = list()
for plc in plc_list:
    slc_insert.append(plc.__dict__)
plc_list = list()

print('\n-------\nwrite data records')

today = datetime.datetime.now().date()
counter = 0
with sqlite3.connect("../common/data/open-railway.sqlite",
                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("delete from 'crd.slc'")
    cursor.executemany('INSERT INTO "crd.slc" '
                       '(Country_ISO_Code, Responsible_IM_Code, Subsidiary_Location_Code,'
                       'Location_Code, Subsidiary_Type_Code, Subsidiary_Location_Name,'
                       'Start_Validity, AllocationCompany, Active_Flag, Add_Date,'
                       'Modified_Date, End_Validity, Free_Text, Latitude, Longitude) '
                       'VALUES'
                       '(:Country_ISO_Code, :Responsible_IM_Code, '
                       ':Subsidiary_Location_Code,'
                       ':Location_Code, :Subsidiary_Type_Code, :Subsidiary_Location_Name,'
                       ':Start_Validity, :AllocationCompany, :Active_Flag, :Add_Date,'
                       ':Modified_Date, :End_Validity, :Free_Text, :Latitude, :Longitude)'
                       , slc_insert)
    conn.commit()

    print(f"SLC: {len(slc_insert)} data records were written")
