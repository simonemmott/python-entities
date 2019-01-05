'''
Created on 16 Dec 2018

@author: simon
'''
from functools import wraps
from utilities import classUtil, typeUtil
import json

_pkFunctions = {}
_entities = {}

def entity(**kw):
    def decorator(cls):
        entityName = kw.get('name', cls.__name__)
        _entities[entityName] = cls
        key = kw.get('key')
        cls.__Entity__ = {}
        cls.__Entity__['name'] = entityName
        cls.__Entity__['key'] = key
        cls.__Entity__['discriminator'] = kw.get('discriminator')
        
        for name in classUtil.get_attributes(cls):
            attr = getattr(cls, name)
            attr.name = name
            if isinstance(attr, EmbeddedAttribute):
                class MethodBuilder(object):
                    def __init__(self, name, cls):
                        @classUtil.add_named_method('add_to_'+name, cls)
                        def add_to(self, *items):
                            embedded = getattr(self, name)
                            if not embedded:
                                embedded = []
                            for item in items:
                                item.__domain_parent__ = self
                                embedded.append(item)
                            setattr(self, name, embedded)
                MethodBuilder(name, cls)
            
        @classUtil.add_method(cls)
        def _json(self, **kw):
            if kw.get('pretty'):
                return json.dumps(typeUtil.to_dict(self), indent=kw.get('indent',4))
            else:
                return json.dumps(typeUtil.to_dict(self))
            
        if key:
            @classUtil.add_method(cls)
            def __eq__(self, obj):
                if id(self) == id(obj):
                    return True
                if not isinstance(obj, cls):
                    return False
                if self.__pk__() != obj.__pk__():
                    return False
                return True            
            
            @classUtil.add_method(cls)
            def __pk__(self):
                pkey = ()
                if isinstance(key, str):
                    try:
                        pkey = pkey + (getattr(self, '_'+key),)
                    except(AttributeError):
                        pkey = pkey + (getattr(self, key),)
                elif isinstance(key, tuple):
                    for attr in key:
                        try:
                            pkey = pkey + (getattr(self, '_'+attr),)
                        except(AttributeError):
                            pkey = pkey + (getattr(self, attr),)
                return pkey
            _pkFunctions[entityName] = __pk__
                        
        @classUtil.add_method(cls)
        def __domain_root__(self):
            root = self
            while hasattr(root, '__domain_parent__') and root.__domain_parent__:
                root = root.__domain_parent__
            return root

           
        return cls
                
    return decorator

def get_pk(obj):
    ancestor = get_ancestor_entity(obj.__class__)
    pk = _pkFunctions.get(ancestor.__Entity__['name'])
    return pk(obj) if pk else None

def get_entity(entityName):
    return _entities.get(entityName)

def is_entity(cls):
    try:
        return cls.__Entity__ != None
    except(AttributeError):
        return False
    
def add_to_list(obj, list_name, *items):
    embedded = getattr(obj, list_name)
    if not embedded:
        embedded = []
    for item in items:
        item.__domain_parent__ = obj
        embedded.append(item)
    setattr(obj, list_name, embedded)
    
    
def is_entity_instance(obj):
    return is_entity(obj.__class__)

def get_entity_name(cls):
    if is_entity(cls):
        return cls.__Entity__['name']
    raise ValueError('The given class: %s is not an entity' % cls.__name__)

def get_super_entity(cls):
    if not cls.__bases__:
        return None
    sup = cls.__bases__[0]
    if sup == Entity:
        return None
    if is_entity(sup):
        return sup
    return get_super_entity(sup)

def get_ancestor_entity(cls):
    sup = get_super_entity(cls)
    if not sup:
        return cls
    return get_ancestor_entity(sup)
    
class Entity(object):
    
    def __init__(self, **kw):
        for attr in classUtil.get_attributes(self.__class__):
            if attr[0] == '_':
                key = attr[1:]
            else:
                key = attr
            a = getattr(self.__class__, attr)
            if not a:
                setattr(self, attr, kw.get(key, None))
            elif isinstance(a, EmbeddedAttribute):
                items = kw.get(key,[])
                for item in items:
                    item.__domain_parent__ = self
                setattr(self, attr, items)
            else:
                setattr(self, attr, kw.get(key, None))

class Attribute(object):
    def __init__(self, data_type, **kw):
        self.data_type = data_type
        self.title = kw.get('title')
        self.description = kw.get('description')
    
    @staticmethod
    def discriminator(**kw):
        return Attribute(str, **kw)
        
    @staticmethod
    def string(**kw):
        return Attribute(str, **kw)
        
    @staticmethod
    def number(**kw):
        return Attribute(int, **kw)
        
    @staticmethod
    def decimal(**kw):
        return Attribute(float, **kw)
        
    @staticmethod
    def boolean(**kw):
        return Attribute(bool, **kw)
        
    @staticmethod
    def structured(data_type, **kw):
        return Attribute(data_type, **kw)
        
    @staticmethod
    def linked(data_type, **kw):
        return Attribute(data_type, **kw)
        
    @staticmethod
    def embedded(data_type, **kw):
        return EmbeddedAttribute(data_type, **kw)
        
    @staticmethod
    def list(data_type, **kw):
        return Attribute(data_type, **kw)
        
class EmbeddedAttribute(Attribute):
    pass
    



