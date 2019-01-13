'''
Created on 26 Dec 2018

@author: simon
'''
import entities, copy, itertools, threading, json, hashlib
from entities import diff
from utilities import classUtil

class CacheError(Exception):
    pass

class Cache(object):

    def __init__(self, *args, **kw):
        self._cache = {}
        
    def _ancestor_cache(self, ancestor):
        ancestor_cache = self._cache.get(ancestor)
        if not ancestor_cache:
            ancestor_cache = {}
            self._cache[ancestor] = ancestor_cache
        return ancestor_cache
    
    def put(self, obj):
        ancestor_cache = self._ancestor_cache(entities.get_ancestor_entity(obj.__class__))
        pk = entities.get_pk(obj)
        ancestor_cache[pk] = obj
        return obj
        
    def get(self, entity, *keys):
        if len(keys) == 0:
            raise KeyError('Unable to fetch entities of type %s without a key' % entities.get_entity_name(entity))
        elif len(keys) == 1:
            key = keys[0]
            if not isinstance(key, tuple):
                key = (key,)
        else:
            key = ()
            for k in keys:
                if isinstance(k, tuple):
                    key = key + k
                else:
                    key = key + (k,)

        ancestor_cache = self._ancestor_cache(entities.get_ancestor_entity(entity))
        e = ancestor_cache.get(key)
        if not e:
            raise KeyError('No entity of type %s found with key %s' % (entity, key))
        return e
    
    def remove(self, obj):
        ancestor_cache = self._ancestor_cache(entities.get_ancestor_entity(obj.__class__))
        del ancestor_cache[entities.get_pk(obj)]
        return obj
        
    def list(self, entity):
        ancestor_entity = entities.get_ancestor_entity(entity)
        ancestor_cache = self._ancestor_cache(ancestor_entity)
        lst = []
        for e in ancestor_cache.values():
            if isinstance(e, entity):
                lst.append(e)
        return lst
    
    def list_types(self):
        return self._cache.keys()

class LinkedCache(Cache):
    def __init__(self, source, **kw):
        Cache.__init__(self, **kw)
        self.source = source
        self.removed = []

    def put(self, obj):
        if obj in self.removed:
            self.removed.remove(obj)
        return Cache.put(self, obj)
    
    def get(self, entity, *keys):
        try:
            return Cache.get(self, entity, *keys)
        except KeyError:
            hit = self.source.get(entity, *keys)
            if hit not in self.removed:
                Cache.put(self, hit)
                return hit
    
    def remove(self, obj):
        if obj in self.removed:
            return obj
        self.removed.append(obj)
        return Cache.remove(self, obj)
    
    def list(self, entity):
        cache_lst =  Cache.list(self, entity)
        for item in self.source.list(entity):
            if item not in cache_lst and item not in self.removed:
                cache_lst.append(item)
        return cache_lst
    
    def push(self):
        for cls in self.list_types():
            print('Pushing caches for type %s' % cls)
            for obj in self.list(cls):
                self.source.put(obj)
        for removed in self.removed:
            self.source.remove(removed)
        self.clear()
        
    def clear(self):
        self._cache = {}
        self.removed = []
        
        