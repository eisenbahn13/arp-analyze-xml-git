import xml.parsers.expat
import utils

# contains the actual parents
parent_elem = list()

# contains the tree statistic
xml_tree = dict()

counter = 0


def monitor_parser():
    global counter
    counter += 1
    if (counter % 5) == 0:
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
    # print(p_str, '+', attrs)
    monitor_parser()


def end_element(name):
    # print('/'.join(parent_elem), '-')
    parent_elem.pop()


def char_data(data: str):
    if len(data.strip()) > 0:
        pass
        # print('Character data:', repr(data))


p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

print('\n--------------')
# open the zipfile and parse the xml
file_name = "data/example-03.xml"
with open(file_name, "rb") as file:
    print(file.read(100))
print('\n--------------')
with open(file_name, "rb") as file:
    p.ParseFile(file)

print('\n--------------')
root = utils.reformat_xml_tree(xml_tree)
utils.print_nodes(root)
print('\n--------------')
xml_str = utils.to_xml(root)
print(xml_str)
with open('data/result_example-02.xml', 'w') as file:
    file.write(xml_str)
