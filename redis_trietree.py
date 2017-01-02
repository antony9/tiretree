from trietree import Node


def get_node_value(node):
    if isinstance(node, Node):
        if node.value == node.DUMMY_VALUE:
            v = RedisNode.DUMMY_VALUE
        else:
            v = node.value
    else:
        v = RedisNode.DUMMY_VALUE
    return v


class RedisNodeChildrenDict(object):
    """
    define a dict-like object to operated on a certain redis
      key: the key of the node
      children_key : key:children
      contains: children_key exists
      getitem: return a redis node of children_key
      setitem: create a children key, with a certain value
    """

    def __init__(self, current_node):
        self._node = current_node

    def __contains__(self, child):
        return self._node._rds_.exists("%s:%s" % (self._node.get_rds_key(), child))

    def __setitem__(self, k, node):
        if isinstance(node, Node):
            v = get_node_value(node)
            self._node._rds_.set("%s:%s" % (self._node.get_rds_key(), k), v)
        else:
            raise RuntimeError()

    def __getitem__(self, k):
        # Just return a node, don't care the value
        return RedisNode(self._node, k, RedisNode.DUMMY_VALUE, set_value=False)


class RedisNode(Node):
    _rds_ = None
    DUMMY_VALUE = '-1'

    @classmethod
    def init_redis(cls, rds, prefix):
        cls._rds_ = rds
        cls._prefix_ = prefix

    def __init__(self, parent, key, value, set_value=True):
        if parent is None and key is None:
            self._rds_key = "%s" % self._prefix_
        else:
            self._rds_key = "%s:%s" % (parent.get_rds_key(), key)

        if not set_value:
            return

        if value is None:
            value = self.DUMMY_VALUE
        else:
            value = get_node_value(value)

        # for value, set it
        self._rds_.set(self._rds_key, value)

    def get_rds_key(self):
        return self._rds_key

    @property
    def children(self):
        return RedisNodeChildrenDict(self)

    @property
    def value(self):
        ret = self._rds_.get(self._rds_key)
        return ret

    @value.setter
    def value(self, value):
        self._rds_.set(self._rds_key, value)
