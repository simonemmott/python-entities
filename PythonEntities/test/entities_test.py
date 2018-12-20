'''
Created on 16 Dec 2018

@author: simon
'''
from entities import entities
from utilities import classUtil
import unittest, json


@entities.entity(
    name='ENTITY_A',
    key=('id'))
class EntityA(object):
    
    _id = None
    _name = None
    _description = None
    
    def __init__(self, **kw):
        self._id = kw.get('id', self._id)
        self._name = kw.get('name', self._name)
        self._description = kw.get('description', self._description)
        
        
@entities.entity(
    key=('package', 'name'))
class TypeA(object):
    
    _package = None
    _name = None
    _description = None
    
    def __init__(self, **kw):
        self._package = kw.get('package', self._package)
        self._name = kw.get('name', self._name)
        self._description = kw.get('description', self._description)
        
class ClassA(object):
    
    _name = None
    _description = None
    
    def __init__(self, **kw):
        self._name = kw.get('name', self._name)
        self._description = kw.get('description', self._description)
        
class TestEntities(unittest.TestCase):

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
        assert eA._pk() == (123,)
        
        tA = TypeA(
            package='aaa.bbb.ccc',
            name='ddd',
            description='TypeA at aaa.bbb.ccc.ddd')
        
        assert entities.get_pk(tA) == ('aaa.bbb.ccc', 'ddd')
        assert tA._pk() == ('aaa.bbb.ccc', 'ddd')
        
    def test_is_entity(self):
        assert entities.is_entity(EntityA)
        assert entities.is_entity(TypeA)
        assert not entities.is_entity(ClassA)

     
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
                 
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNewArm']
    unittest.main()