class Node(object):
    no_value = object()

    def _get_key(self, root):
        k = []
        n = self
        while n is not root:
            k.append(n.key)
            n = n.parent
        k.reverse()
        return k

    def __init__(self, parent, key, children, value):
        self.parent = parent
        self.key = key
        self.children = children
        self.value = value


class Trie(object):
    """
    Trie algorithm implemetation.
    """

    def __init__(self, root_data=None, mapping={}):
        self.root = Node(None, None, {}, root_data)
        if mapping:
            self.extend(mapping)

    def extend(self, mapping):
        for (k, v) in mapping.items():
            self[k] = v

    def __setitem__(self, k, v):
        n = self.root
        for c in str(k):
            n = n.children.setdefault(c, Node(n, c, {}, Node.no_value))
        n.value = v

    def match(self, k):
        ret = Node.no_value
        n = self.root
        for c in str(k):
            if c in n.children:
                n = n.children[c]
                if n.value is not Node.no_value:
                    ret = n.value
            else:
                break
        if ret is Node.no_value:
            raise KeyError(k)

        return ret
