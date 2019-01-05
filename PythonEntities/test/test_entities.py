'''
Created on 16 Dec 2018

@author: simon
'''

from entities import entity, Entity, Attribute

@entity(
    name='ENTITY_A',
    key=('id'),
    discriminator='a_type')
class EntityA(Entity):
    _id = Attribute.number()
    _name = Attribute.string(title="The Name")
    _description = Attribute.string(title="The Description")
    _a_type = Attribute.discriminator()
            
        
@entity(name='ENTITY_AB')
class EntityAB(EntityA):
    _age = Attribute.number()
    _ab_type = Attribute.discriminator()
    
        
@entity(name='ENTITY_ABC')
class EntityABC(EntityAB):  
    _colour = Attribute.string()
    
        
@entity(
    name='ENTITY_B',
    key=('package', 'name'),
    discriminator='type')
class EntityB(Entity):
    _package = Attribute.string()
    _name = Attribute.string()
    _description = Attribute.string()
    _b_type = Attribute.discriminator()
            
        
@entity(name='ENTITY_BA')
class EntityBA(EntityB):  
    _age = Attribute.number()
    _ba_type = Attribute.discriminator()    
        
@entity(name='ENTITY_BAB')
class EntityBAB(EntityBA):
    _colour = Attribute.string()
    
        
@entity(key=('package', 'name'))
class TypeA(Entity):
    _package = Attribute.string()
    _name = Attribute.string()
    _description = Attribute.string()
    

@entity(
    name='ENTITY_C',
    key=('id'),
    discriminator='a_type')
class EntityC(Entity):
    id = Attribute.number()
    name = Attribute.string(title="The Name")
    description = Attribute.string(title="The Description")

@entity(key=('id'))
class ChildEntity(Entity):
    _id = Attribute.number()
    _name = Attribute.string()
                            

@entity(key=('id'))
class ParentEntity(Entity):
    _id = Attribute.number()
    _name = Attribute.string()
    _children = Attribute.embedded(ChildEntity)
            

@entity(key=('id'))
class RootEntity(Entity):
    _id = Attribute.number()
    _name = Attribute.string()
    _children = Attribute.embedded(ParentEntity)
            
