'''
Created on 16 Dec 2018

@author: simon
'''

import entities
import unittest, json
from test_entities import *

        
class ClassA(Entity):
    _name = None
    _description = None

        
class TestEntities(unittest.TestCase):
    
    def test_get_super_entity(self):
        self.assertEqual(EntityA, entities.get_super_entity(EntityAB))
        self.assertEqual(EntityB, entities.get_super_entity(EntityBA))

    def test_get_ancestor_entity(self):
        self.assertEqual(EntityA, entities.get_ancestor_entity(EntityA))
        self.assertEqual(EntityA, entities.get_ancestor_entity(EntityAB))
        self.assertEqual(EntityA, entities.get_ancestor_entity(EntityABC))

    def test_entity_name(self):
        
        eA = EntityA(
            id=123,
            name='Entity A',
            description='Entity A description')

        
        assert eA.__class__.__Entity__['name'] == 'ENTITY_A'
        
        tA = TypeA(
            package='aaa.bbb.ccc',
            name='ddd',
            description='TypeA at aaa.bbb.ccc.ddd')
        
        assert tA.__class__.__Entity__['name'] == 'TypeA'

        
    def test_pk(self):
        
        eA = EntityA(
            id=123,
            name='Entity A',
            description='Entity A description')

        assert entities.get_pk(eA) == (123,)
        assert eA.__pk__() == (123,)
        
        tA = TypeA(
            package='aaa.bbb.ccc',
            name='ddd',
            description='TypeA at aaa.bbb.ccc.ddd')
        
        assert entities.get_pk(tA) == ('aaa.bbb.ccc', 'ddd')
        assert tA.__pk__() == ('aaa.bbb.ccc', 'ddd')
        
        eABC = EntityABC(
            id=123,
            name='Entity A',
            description='Entity A description')

        self.assertEquals((123,), entities.get_pk(eABC))
        self.assertEquals((123,), eABC.__pk__())
        
    def test_equality(self):
        
        re1_a = RootEntity(id=1, name='Fred')
        re1_b = RootEntity(id=1, name='Barny')
        
        self.assertEqual(re1_a, re1_b)
        
        eb_a = EntityB(package='pack', name='name')
        eb_b = EntityB(package='pack', name='name')
        eb_c = EntityB(package='pack', name='xxxx')

        self.assertEqual(eb_a, eb_b)
        self.assertNotEqual(eb_a, eb_c)
        
    def test_is_entity(self):
        assert entities.is_entity(EntityA)
        assert entities.is_entity(TypeA)
        assert not entities.is_entity(ClassA)

    def test_is_entity_instance(self):
        eA = EntityA(
            id=123,
            name='Entity A',
            description='Entity A description')
        cA = ClassA(name='Class A', description='Description of class A')
        
        self.assertTrue(entities.is_entity_instance(eA))
        self.assertFalse(entities.is_entity_instance(cA))
     
    def test_get_entity_name(self):
        assert entities.get_entity_name(EntityA) == 'ENTITY_A'
        assert entities.get_entity_name(TypeA) == 'TypeA'   
        
    def test_get_entity(self):
        assert entities.get_entity('ENTITY_A') == EntityA
        assert entities.get_entity('TypeA') == TypeA
        
    def test_json(self):
        
        eA = EntityA(
            id=123,
            name='Entity A',
            description='Entity A description')
        
        JSON = eA._json()
        DICT = json.loads(JSON)
        
        assert DICT['_description'] == 'Entity A description'
        assert DICT['_id'] == 123
        assert DICT['_name'] == 'Entity A'
                 
    def test_attributes(self):

        eA = EntityA(
            id=123,
            name='Entity A',
            description='Entity A description')
        
        self.assertTrue(isinstance(EntityA._id, Attribute))
        self.assertTrue(isinstance(eA.__class__._id, Attribute))
        self.assertTrue(isinstance(EntityA._name, Attribute))
        self.assertEqual(EntityA._name.title, 'The Name')
        self.assertEqual(EntityA._description.title, 'The Description')
        
    def test_attribute_name(self):
        self.assertEqual(RootEntity._id.name, '_id')
        self.assertEqual(RootEntity._name.name, '_name')
        self.assertEqual(RootEntity._children.name, '_children')
    
    def test_parent_root(self):
                
        pe1 = ParentEntity(id=1, name='Parent Entity 1')
        pe2 = ParentEntity(id=2, name='Parent Entity 2')
        re = RootEntity(id=1, name='Root Entity', children=[pe1, pe2])
        
        self.assertEqual(re, re.__domain_root__())
        self.assertEqual(re, pe1.__domain_root__())
        self.assertEqual(re, pe2.__domain_root__())
        
        self.assertEqual(re, pe1.__domain_parent__)
        self.assertEqual(re, pe2.__domain_parent__)
        
        ce_1 = ChildEntity(id=1, name='Child Entity 1')
        ce_2 = ChildEntity(id=2, name='Child Entity 2')

        pe3 = ParentEntity(id=3, name='Parent Entity 3')
        
        self.assertFalse(hasattr(pe3, '__domain_parent__'))

        re.add_to__children(pe3)
        
        self.assertEqual(re, pe3.__domain_parent__)
        self.assertEqual(re, pe3.__domain_root__())
        
        ce_3 = ChildEntity(id=3, name='Child Entity 3')

        pe3.add_to__children(ce_1, ce_2, ce_3)

        self.assertEqual(pe3, ce_1.__domain_parent__)
        self.assertEqual(pe3, ce_2.__domain_parent__)
        self.assertEqual(pe3, ce_3.__domain_parent__)
        self.assertEqual(re, ce_1.__domain_root__())
        self.assertEqual(re, ce_2.__domain_root__())
        self.assertEqual(re, ce_3.__domain_root__())
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNewArm']
    unittest.main()