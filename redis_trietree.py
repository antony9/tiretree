from trietree import Node


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
        return self._node._rds_.exists("%s:%s" % (self._key, child))

    def __setitem__(self, k, node):
        if isinstance(node, Node):
            if node.value is node.DUMMY_VALUE:
                v = RedisNode.DUMMY_VALUE
            else:
                v = node.value

            self._node._rds_.set("%s:%s" % (self._key, k), v)
        else:
            raise RuntimeError()

    def __getitem__(self, k):
        return RedisNode(self._node, k, set_value=False)


class RedisNode(Node):
    _rds_ = None
    DUMMY_VALUE = '-1'

    @classmethod
    def init_redis(cls, rds, prefix):
        cls._rds_ = rds
        cls._prefix_ = prefix

    def __init__(self, parent, key, value, set_value=True):
        if parent is None:
            parent_prefix = self._prefix_
        else:
            parent_prefix = parent.get_rds_key()
        self._rds_key = "%s:%s" % (parent_prefix, key)

        if not set_value:
            return

        if value is None:
            value = self.DUMMY_VALUE

        # for value, set it
        self._rds_.set(self._rds_key, value)

    def get_rds_key(self):
        return self._rds_key

    @property
    def children(self):
        return RedisNodeChildrenDict(self._rds_, self._rds_key)

    @property
    def value(self):
        return self._rds_.get(self._rds_key)

    @value.setter
    def value(self, value):
        self._rds_.set(self._rds_key, value)
