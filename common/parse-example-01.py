import xml.parsers.expat
from zipfile import ZipFile


# import gzip


# 3 handler functions
def start_element(name, attrs):
    print('Start element:', name, attrs)


def end_element(name):
    print('End element:', name)


def char_data(data):
    print('Character data:', repr(data))


p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

# p.Parse("""<?xml version="1.0"?>
# <parent id="top"><child1 name="paul">Text goes here</child1>
# <child2 name="fred">More text</child2>
# </parent>""", 1)

'''
file_name = "data/example-01.xml"

# read the file
with open(file_name, "rb") as file:
    print(file.read())

# parse the file as xml
with open(file_name, "rb") as file:
    p.ParseFile(file)
'''

# open the zipfile and parse the xml
zfile_name = "data/example-01.zip"
file_name = "example-01.xml"
#zfile = ZipFile(zfile_name, 'r')
with ZipFile(zfile_name, "r") as zfile:
    with zfile.open(file_name, "r") as file:
        p.ParseFile(file)
