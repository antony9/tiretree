import unittest
import redis

from trietree import Trie
from redis_trietree import RedisNode


class TestTireTree(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()

    def tearDown(self):
        del self.trie

    def test_sanity(self):
        self.trie['abc'] = '10'
        self.trie['abcd'] = '11'
        self.assertEqual(self.trie.match('abcdefghijk'), '11')
        self.assertEqual(self.trie.match('abcefg'), '10')

    def test_hole(self):
        self.trie['135'] = '10'
        self.trie['1351008'] = '100'
        self.assertEqual(self.trie.match('13510071234'), '10')
        self.assertEqual(self.trie.match('13510081234'), '100')

    def test_load(self):
        trie = Trie(mapping={'135': '100', '136': '101'})
        self.assertEqual(trie.match('13510000000'), '100')
        self.assertEqual(trie.match('13610000000'), '101')

    def test_only_one(self):
        self.trie['1'] = '0.02'
        self.trie['1358'] = '11'
        self.assertEqual(self.trie.match('135810001000'), '11')
        self.assertEqual(self.trie.match('135210001000'), '0.02')


class TestRedisTrieTree(TestTireTree):
    def setUp(self):
        self.rds = redis.Redis()
        RedisNode.init_redis(self.rds, "RedisPrefix")
        self.trie = Trie(node_class=RedisNode)

    def tearDown(self):
        keys = self.rds.keys("RedisPrefix*")
        for k in keys:
            self.rds.delete(k)

    def test_load(self):
        trie = Trie(mapping={'135': '100', '136': '101'}, node_class=RedisNode)
        self.assertEqual(trie.match('13510000000'), '100')
        self.assertEqual(trie.match('13610000000'), '101')

if __name__ == '__main__':
    unittest.main()
