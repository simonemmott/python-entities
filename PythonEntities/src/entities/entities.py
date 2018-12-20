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
            
        @classUtil.add_method(cls)
        def _json(self, **kw):
            if kw.get('pretty'):
                return json.dumps(typeUtil.to_dict(self), indent=kw.get('indent',4))
            else:
                return json.dumps(typeUtil.to_dict(self))
            
        if key:
            @classUtil.add_method(cls)
            def _pk(self):
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
            _pkFunctions[entityName] = _pk
            
        return cls
                
    return decorator

def get_pk(obj):
    pk = _pkFunctions.get(obj.__class__.__Entity__['name'])
    return pk(obj) if pk else None

def get_entity(entityName):
    return _entities.get(entityName)

def is_entity(cls):
    try:
        return cls.__Entity__ != None
    except(AttributeError):
        return False

def get_entity_name(cls):
    if is_entity(cls):
        return cls.__Entity__['name']
    raise ValueError('The given class: %s is not an entity' % cls.__name__)
