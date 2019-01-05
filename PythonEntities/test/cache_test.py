'''
Created on 16 Dec 2018

@author: simon
'''

import entities, itertools
from entities.cache import Cache, CommitCache, ServerCache, get_entity, commit_ref
import unittest
from test_entities import *
                
class TestCache(unittest.TestCase):
    
    def test_new_cache(self):
        cache = Cache()
        self.assertNotEqual(None, cache)
        self.assertTrue(isinstance(cache, Cache))

    def test_ancestor_cache(self):
        cache = Cache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        cache.put(eA1)
        
        root_cache = cache._ancestor_cache(EntityA)
        self.assertNotEqual(None, root_cache)
        self.assertEqual(1, len(root_cache))
        
    def test_get(self): 
        cache = Cache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        eA2 = EntityA(id=2, name='EntityA 2') 
        cache.put(eA1)
        cache.put(eA2)
        self.assertEqual(eA1, cache.get(EntityA, 1))
        self.assertEqual(eA1, cache.get(EntityA, (1,)))
        self.assertEqual(eA2, cache.get(EntityA, 2))
        self.assertEqual(eA2, cache.get(EntityA, (2,)))
             
        eB1 = EntityB(package='pack', name='EntityB 1') 
        eB2 = EntityB(package='pack', name='EntityB 2') 
        cache.put(eB1)
        cache.put(eB2)
        self.assertEqual(eB1, cache.get(EntityB, 'pack', 'EntityB 1'))
        self.assertEqual(eB1, cache.get(EntityB, ('pack', 'EntityB 1')))
        self.assertEqual(eB2, cache.get(EntityB, 'pack', 'EntityB 2'))
        self.assertEqual(eB2, cache.get(EntityB, ('pack', 'EntityB 2')))
        
        eABC3 = EntityABC(id=3, name='EntityABC 3') 
        eABC4 = EntityABC(id=4, name='EntityABC 4') 
        cache.put(eABC3)
        cache.put(eABC4)
        self.assertEqual(eABC3, cache.get(EntityABC, 3))
        self.assertEqual(eABC3, cache.get(EntityABC, (3,)))
        self.assertEqual(eABC4, cache.get(EntityABC, 4))
        self.assertEqual(eABC4, cache.get(EntityABC, (4,)))
        self.assertEqual(eABC3, cache.get(EntityA, 3))
        self.assertEqual(eABC3, cache.get(EntityA, (3,)))
        self.assertEqual(eABC4, cache.get(EntityA, 4))
        self.assertEqual(eABC4, cache.get(EntityA, (4,)))

    def test_list(self): 
        cache = Cache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        eA2 = EntityA(id=2, name='EntityA 2') 
        cache.put(eA1)
        cache.put(eA2) 
                    
        eB1 = EntityB(package='pack', name='EntityB 1') 
        eB2 = EntityB(package='pack', name='EntityB 2') 
        cache.put(eB1)
        cache.put(eB2)
        
        eABC3 = EntityABC(id=3, name='EntityABC 3') 
        eABC4 = EntityABC(id=4, name='EntityABC 4') 
        cache.put(eABC3)
        cache.put(eABC4)

        self.assertEqual(4, len(cache.list(EntityA)))
        self.assertEqual(2, len(cache.list(EntityB)))
        self.assertEqual(2, len(cache.list(EntityAB)))
        self.assertEqual(2, len(cache.list(EntityABC)))
        
        self.assertTrue(eA1 in cache.list(EntityA))
        self.assertTrue(eA2 in cache.list(EntityA))
        self.assertTrue(eABC3 in cache.list(EntityA))
        self.assertTrue(eABC4 in cache.list(EntityA))
        
        self.assertTrue(eB1 in cache.list(EntityB))
        self.assertTrue(eB2 in cache.list(EntityB))

        self.assertTrue(eABC3 in cache.list(EntityAB))
        self.assertTrue(eABC4 in cache.list(EntityAB))
             
        self.assertTrue(eABC3 in cache.list(EntityABC))
        self.assertTrue(eABC4 in cache.list(EntityABC))
        
    def test_remove(self): 
        cache = Cache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        eA2 = EntityA(id=2, name='EntityA 2') 
        cache.put(eA1)
        cache.put(eA2) 
                            
        self.assertNotEqual(None, cache.get(EntityA, 1))
        cache.remove(eA1)
        try:
            cache.get(EntityA, 1)
            self.fail('Key error expected')
        except(KeyError):
            pass
        except:
            self.fail('Key error expected')
            
        self.assertEqual(1, len(cache.list(EntityA)))
        
        
class TestCommitCache(unittest.TestCase):
    
    def test_new_cache(self):
        cache = CommitCache()
        self.assertNotEqual(None, cache)
        self.assertTrue(isinstance(cache, CommitCache))

    def test_ancestor_cache(self):
        cache = CommitCache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        cache.put(eA1)
        
        root_cache = cache._ancestor_cache(EntityA)
        self.assertNotEqual(None, root_cache)
        self.assertEqual(1, len(root_cache))
        
    def test_get(self): 
        cache = CommitCache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        eA2 = EntityA(id=2, name='EntityA 2') 
        cache.put(eA1)
        cache.put(eA2)
        self.assertEqual(eA1, cache.get(EntityA, 1))
        self.assertEqual(eA1, cache.get(EntityA, (1,)))
        self.assertEqual(eA2, cache.get(EntityA, 2))
        self.assertEqual(eA2, cache.get(EntityA, (2,)))
             
        eB1 = EntityB(package='pack', name='EntityB 1') 
        eB2 = EntityB(package='pack', name='EntityB 2') 
        cache.put(eB1)
        cache.put(eB2)
        self.assertEqual(eB1, cache.get(EntityB, 'pack', 'EntityB 1'))
        self.assertEqual(eB1, cache.get(EntityB, ('pack', 'EntityB 1')))
        self.assertEqual(eB2, cache.get(EntityB, 'pack', 'EntityB 2'))
        self.assertEqual(eB2, cache.get(EntityB, ('pack', 'EntityB 2')))
        
        eABC3 = EntityABC(id=3, name='EntityABC 3') 
        eABC4 = EntityABC(id=4, name='EntityABC 4') 
        cache.put(eABC3)
        cache.put(eABC4)
        self.assertEqual(eABC3, cache.get(EntityABC, 3))
        self.assertEqual(eABC3, cache.get(EntityABC, (3,)))
        self.assertEqual(eABC4, cache.get(EntityABC, 4))
        self.assertEqual(eABC4, cache.get(EntityABC, (4,)))
        self.assertEqual(eABC3, cache.get(EntityA, 3))
        self.assertEqual(eABC3, cache.get(EntityA, (3,)))
        self.assertEqual(eABC4, cache.get(EntityA, 4))
        self.assertEqual(eABC4, cache.get(EntityA, (4,)))

    def test_list(self): 
        cache = CommitCache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        eA2 = EntityA(id=2, name='EntityA 2') 
        cache.put(eA1)
        cache.put(eA2) 
                    
        eB1 = EntityB(package='pack', name='EntityB 1') 
        eB2 = EntityB(package='pack', name='EntityB 2') 
        cache.put(eB1)
        cache.put(eB2)
        
        eABC3 = EntityABC(id=3, name='EntityABC 3') 
        eABC4 = EntityABC(id=4, name='EntityABC 4') 
        cache.put(eABC3)
        cache.put(eABC4)

        self.assertEqual(4, len(cache.list(EntityA)))
        self.assertEqual(2, len(cache.list(EntityB)))
        self.assertEqual(2, len(cache.list(EntityAB)))
        self.assertEqual(2, len(cache.list(EntityABC)))
        
        self.assertTrue(eA1 in cache.list(EntityA))
        self.assertTrue(eA2 in cache.list(EntityA))
        self.assertTrue(eABC3 in cache.list(EntityA))
        self.assertTrue(eABC4 in cache.list(EntityA))
        
        self.assertTrue(eB1 in cache.list(EntityB))
        self.assertTrue(eB2 in cache.list(EntityB))

        self.assertTrue(eABC3 in cache.list(EntityAB))
        self.assertTrue(eABC4 in cache.list(EntityAB))
             
        self.assertTrue(eABC3 in cache.list(EntityABC))
        self.assertTrue(eABC4 in cache.list(EntityABC))
        
    def test_remove(self): 
        cache = CommitCache() 
         
        eA1 = EntityA(id=1, name='EntityA 1') 
        eA2 = EntityA(id=2, name='EntityA 2') 
        eA1 = cache.put(eA1)
        eA2 = cache.put(eA2) 
                            
        self.assertNotEqual(None, cache.get(EntityA, 1))
        cache.remove(eA1)
        try:
            cache.get(EntityA, 1)
            self.fail('Key error expected')
        except(KeyError):
            pass
        except:
            self.fail('Key error expected')
            
        self.assertEqual(1, len(cache.list(EntityA)))


class TestServerCache(unittest.TestCase):
    
    def test_new_server_cache(self):
        sc = ServerCache()
        self.assertNotEqual(None, sc)
        self.assertTrue(isinstance(sc, ServerCache))
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNewArm']
    unittest.main()