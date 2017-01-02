class Node(object):
    DUMMY_VALUE = object()

#    def _get_key(self, root):
#        k = []
#        n = self
#        while n is not root:
#            k.append(n.key)
#            n = n.parent
#        k.reverse()
#        return k

    def __init__(self, parent, key, value):
        self._key = key
        self._children = {}
        self._value = value

    @property
    def children(self):
        return self._children

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Trie(object):
    """
    Trie algorithm implemetation.
    """

    def __init__(self, root_data=None, mapping={}, key_split_callback=None, node_class=Node):
        self.key_split_callback = key_split_callback
        self.node_class = Node
        self.root = self.node_class(None, None, root_data)
        if mapping:
            self.extend(mapping)

    def extend(self, mapping):
        for (k, v) in mapping.items():
            self[k] = v

    def __get_key_split(self, k):
        key_split_result = []
        if self.key_split_callback:
            key_split_result = self.key_split_callback(k)
        else:
            key_split_result = list(str(k))
        return key_split_result

    def __setitem__(self, k, v):
        n = self.root
        key_split_result = self.__get_key_split(k)
        for c in key_split_result:
            if c not in n.children:
                n.children[c] = self.node_class(n, c, Node.DUMMY_VALUE)
            n = n.children[c]
        n.value = v

    def match(self, k):
        ret = Node.DUMMY_VALUE
        n = self.root
        key_split_result = self.__get_key_split(k)
        for c in key_split_result:
            if c in n.children:
                n = n.children[c]
                if n.value is not Node.DUMMY_VALUE:
                    ret = n.value
            else:
                break
        if ret is Node.DUMMY_VALUE:
            raise KeyError(k)

        return ret
