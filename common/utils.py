import xml.dom.minidom


class Node():
    def __init__(self, name: str, count=0):
        self._name = name
        self._count = 1
        self._childs = dict()
        self._attrs = dict()

    def name(self) -> str:
        return self._name

    def count(self) -> int:
        return self._count

    def childs(self) -> dict:
        return self._childs

    def attrs(self) -> dict:
        return self._attrs


def reformat_xml_tree(data: dict) -> dict:
    root = Node('root')
    new_data = dict()
    for key, val in data.items():
        keys = key.split('/')
        # parent_ = k[:-1]
        # leaf_ = k[-1]
        node = get_or_insert_node(root, keys)
        node._count = val['count']
        del val['count']
        node._attrs = val
    return root


def get_or_insert_node(parent_node: Node, keys: list, level=0):
    k = keys[0]
    if k in parent_node.childs():
        if len(keys) > 1:
            return get_or_insert_node(parent_node.childs()[k], keys[1:], level + 1)
        else:
            return parent_node.childs()[k]
    else:
        # create new node child
        new_node = Node(k)
        parent_node.childs()[k] = new_node
        if len(keys) > 1:
            return get_or_insert_node(new_node, keys[1:])
        else:
            return new_node


def print_nodes(node: Node, level=0):
    attrs = ";".join(node.attrs().keys())
    print(f"{level * '  '}- {node.name()} \tcount:{node.count()} attrs:{attrs}")
    for ckey, cnode in node.childs().items():
        print_nodes(cnode, level + 1)


def to_xml(node: Node) -> str:
    def append_node_childs(parent, childs: dict):
        for name, node in childs.items(): # type: str, Node
            name_ = name.split(':')[-1]
            leaf = root.createElement(name_)
            leaf.setAttribute('count', str(node.count()))
            for key, val in node.attrs().items():
                leaf.setAttribute(key, str(val))
            parent.appendChild(leaf)
            if len(node.childs()) > 0:
                append_node_childs(leaf, node.childs())

    root = xml.dom.minidom.Document()

    root_elem = root.createElement(node.name())
    root.appendChild(root_elem)

    append_node_childs(root_elem, node.childs())

    xml_str = root.toprettyxml(indent="\t")

    return xml_str
