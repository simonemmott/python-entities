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

    def __init__(self):
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
        if entity == ancestor_entity:
            return ancestor_cache.values()
        lst = []
        for e in ancestor_cache.values():
            if isinstance(e, entity):
                lst.append(e)
        return lst

class CommitCache(object):

    def __init__(self):
        self._cache = {}
        
    def _ancestor_cache(self, ancestor):
        ancestor_cache = self._cache.get(ancestor)
        if not ancestor_cache:
            ancestor_cache = {}
            self._cache[ancestor] = ancestor_cache
        return ancestor_cache
    
    def transaction(self, old, new):
        if old:
            cref = old._cref_
        else:
            cref = new._cref_
        s = cref+':'+json.dumps(classUtil.to_dict(diff.compare(old, new)))
        return hashlib.md5(s.encode('utf-8')).hexdigest()
    
    def put(self, obj):
        if not hasattr(obj, '_cref_'):
            setattr(obj, '_cref_', 'new')
                     
        ancestor_cache = self._ancestor_cache(entities.get_ancestor_entity(obj.__class__))
        pk = entities.get_pk(obj)
        cached = ancestor_cache.get(pk)
        if not cached or cached._cref_ == obj._cref_:
            if not cached:
                obj._cref_ = self.transaction(None, obj)
            else:
                obj._cref_ = self.transaction(cached, obj)
            ancestor_cache[pk] = obj
            return obj
            
        else:
            raise CacheError("Commit references don't match")
        
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
        pk = entities.get_pk(obj)
        cached = ancestor_cache[pk]
        if cached._cref_ != obj._cref_:
            raise CacheError("Commit references don't match")
        obj._cref_ = self.transaction(cached, None)
        del ancestor_cache[pk]
        return obj
        
    def list(self, entity):
        ancestor_entity = entities.get_ancestor_entity(entity)
        ancestor_cache = self._ancestor_cache(ancestor_entity)
        if entity == ancestor_entity:
            return ancestor_cache.values()
        lst = []
        for e in ancestor_cache.values():
            if isinstance(e, entity):
                lst.append(e)
        return lst

def get_entity(tpl):
    return tpl[0]

def get_commit_ref(tpl):
    return tpl[1]

def commit_ref(trans, cref):
    s = cref+':'+json.dumps(classUtil.to_dict(trans))
    return hashlib.md5(s.encode('utf-8')).hexdigest()
    

class ServerCache(CommitCache):
        
    def session(self):
        local = threading.local()
        if hasattr(local, 'session'):
            return local.session
        s = SessionCache(self)
        local.session = s
        return s
            
class SessionCache(Cache):
    def __init__(self, server):
        self._server = server
        
    def get(self, entity, *keys):
        try:
            return Cache.get(self, entity, *keys)
        except(KeyError):
            e = copy.deepcopy(self._server.get(entity, *keys))
            self.put(e)
            return e
        
    def populate(self, entity):
        lst = Cache.list(self, entity)
        for e in itertools.starmap(copy.deepcopy, self._server.list(entity)):
            if not e in lst:
                lst.append(e)
                self.put(e)
        return lst

    def list(self, entity):
        lst = Cache.list(self, entity)
        for e in self._server.list(entity):
            if not e in lst:
                lst.append(e)
        return lst

        