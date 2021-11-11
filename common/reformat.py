mydict = {'a': {'b': {'c': 1}}}


class Node():
    def __init__(self, name: str, count=1):
        self._name = name
        self._count = 1
        self._childs = dict()

    def name(self) -> str:
        return self._name

    def count(self) ->int:
        return self._count

    def childs(self) -> dict:
        return self._childs


def key_exists(mdict: dict, keys: list):
    k = keys.pop(0)
    if k in mdict:
        if len(keys) > 0:
            try:
                return key_exists(mdict[k], keys)
            except TypeError as e:
                return False
        return True
    else:
        return False


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


print(key_exists(mydict, ['a', 'b']))
print(key_exists(mydict, ['a']))
print(key_exists(mydict, ['a', 'c']))
print(key_exists(mydict, ['a', 'b', 'c']))
print(key_exists(mydict, ['a', 'b', 'c', 'd']))

root = Node('root')
get_or_insert_node(root, ['a'])
t = get_or_insert_node(root, ['a', 'b'])
t._count += 1
get_or_insert_node(root, ['a', 'b', 'c'])
get_or_insert_node(root, ['a', 'd'])


def print_nodes(node: Node, level=0):
    print(f"{level * '  '}- {node.name()} \tcount:{node.count()}")
    for ckey, cnode in node.childs().items():
        print_nodes(cnode, level + 1)




print_nodes(root)
