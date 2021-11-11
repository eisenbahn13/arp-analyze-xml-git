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
class PLC():
    Country_ISO_Code: str = ''
    Location_Code: str = ''
    Country_ISO_code: str = ''
    Location_Code: str = ''
    Start_Validity: str = ''
    End_Validity: str = ''
    Responsible_IM_Code: str = ''
    Location_Name: str = ''
    Location_Name_ASCII: str = ''
    NUTS_Code: str = ''
    Container_Handling_Flag: bool = False
    Handover_Point_Flag: bool = False
    Freight_Possible_Flag: bool = False
    Freight_Start_Validity: str = ''
    Freight_End_Validity: str = ''
    Passenger_Possible_Flag: bool = False
    Passenger_Start_Validity: str = ''
    Passenger_End_Validity: str = ''
    Latitude: float = 0.0
    Longitude: float = 0.0
    Free_Text: str = ''
    Active_Flag: bool = False
    Add_Date: str = ''
    Mod_Date: str = ''


plc_list = list()
focus_lc: PLC = False
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
    if focus_plc:
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
        if focus_plc:
            setattr(focus_plc, focus_plc_elem, data)


p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

print('\n-------')
# open the zipfile and parse the xml
zfile_name = "data/PrimaryLocation v20210812.xml.zip"
file_name = "PrimaryLocation v20210812.xml"
print(f'read file {file_name}')
with ZipFile(zfile_name, "r") as zfile:
    with zfile.open(file_name, "r") as file:
        try:
            p.ParseFile(file)
        except StopException as e:
            print('OK ;-)')

print('-------\nprepare data records')

plc_insert = list()
plc_keys = list()
for plc in plc_list:
    plc_insert.append(plc.__dict__)
plc_list = list()

print('\n-------\nwrite data records')

today = datetime.datetime.now().date()
counter = 0
with sqlite3.connect("../common/data/open-railway.sqlite",
                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("delete from 'crd.plc'")
    cursor.executemany('INSERT INTO "crd.plc" '
                       '(Country_ISO_code, Location_Code, Start_Validity,'
                       'End_Validity, Responsible_IM_Code, Location_Name,'
                       'Location_Name_ASCII, NUTS_Code, Container_Handling_Flag,'
                       'Handover_Point_Flag, Freight_Possible_Flag, '
                       'Freight_Start_Validity,'
                       'Freight_End_Validity, Passenger_Possible_Flag,'
                       'Passenger_Start_Validity, Passenger_End_Validity, Latitude,'
                       'Longitude, Free_Text, Active_Flag, Add_Date, Mod_Date) '
                       'VALUES'
                       '(:Country_ISO_code, :Location_Code, :Start_Validity,'
                       ':End_Validity, :Responsible_IM_Code, :Location_Name,'
                       ':Location_Name_ASCII, :NUTS_Code, :Container_Handling_Flag,'
                       ':Handover_Point_Flag, :Freight_Possible_Flag, '
                       ':Freight_Start_Validity,'
                       ':Freight_End_Validity, :Passenger_Possible_Flag,'
                       ':Passenger_Start_Validity, :Passenger_End_Validity, :Latitude,'
                       ':Longitude, :Free_Text, :Active_Flag, :Add_Date, :Mod_Date)'
                       , plc_insert)
    conn.commit()

print(f"PLC: {len(plc_insert)} data records were written")