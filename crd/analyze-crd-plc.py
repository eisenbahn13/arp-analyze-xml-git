import xml.parsers.expat
from zipfile import ZipFile
from common import utils
import pprint as pp

# contains the actual parents
parent_elem = list()

# contains the tree statistic
xml_tree = dict()

counter = 0

p = xml.parsers.expat.ParserCreate()


def monitor_parser():
    global counter
    counter += 1
    if (counter % 10000) == 0:
        print('.', end='')


# 3 handler functions
def start_element(name, attrs):
    parent_elem.append(name)
    p_str = '/'.join(parent_elem)
    try:
        xml_tree[p_str]['count'] += 1
    except:
        xml_tree[p_str] = {'count': 1}
    for key,val in attrs.items():
        try:
            xml_tree[p_str][key] += 1
        except:
            xml_tree[p_str][key] = 1
    monitor_parser()


def end_element(name):
    # print('/'.join(parent_elem), '-')
    parent_elem.pop()


def char_data(data: str):
    if len(data.strip()) > 0:
        pass
        # print('Character data:', repr(data))


p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

# open the zipfile and parse the xml
#zfile_name = "data/PrilmaryLocation_ALL_ 210527_1441732.zip"
#file_name = "PrilmaryLocation_ALL_ 210527_1441732.xml"
#zfile_name = "data/PrimaryLocation v20210812.xml.zip"
#file_name = "PrimaryLocation v20210812.xml"
zfile_name = "data/SubsidiaryLocation v20210812.xml.zip"
file_name = "SubsidiaryLocation v20210812.xml"

with ZipFile(zfile_name, "r") as zfile:
    with zfile.open(file_name, "r") as file:
        p.ParseFile(file)

print('\n-------')
pp.pprint(xml_tree)
print('\n--------------')
root = utils.reformat_xml_tree(xml_tree)
utils.print_nodes(root)
print('\n--------------')
xml_str = utils.to_xml(root)
print(xml_str)
with open('data/result-plc.xml','w') as file:
    file.write(xml_str)

