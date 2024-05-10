from pychunk.nodes.base import BaseNode
from pychunk.nodes.types import (NodeRelationshipType, 
                                 NodeType)

from typing import (Dict,
                    Any, 
                    Optional, 
                    Type, 
                    List)


class FunctionNode(BaseNode):
    
     def __init__(self, 
                  text: str, 
                  file: str, 
                  node_type: NodeType, 
                  metadata: Optional[Dict[str, Any]] | None = None, 
                  id: Optional[str] | None = None, 
                  node_relationships: Optional[Dict[NodeRelationshipType, List[Type['BaseNode']] | Type['BaseNode']]] | None = None):
        
        super(FunctionNode, self).__init__(text=text, metadata=metadata, id=id, node_relationships=node_relationships, node_type=node_type, file=file)
        
    
class MethodNode(BaseNode):
    
     def __init__(self, 
                  text: str, 
                  file: str, 
                  node_type: NodeType, 
                  metadata: Optional[Dict[str, Any]] | None = None, 
                  id: Optional[str] | None = None, 
                  node_relationships: Optional[Dict[NodeRelationshipType, Type['BaseNode']]] | None = None):
        
        super(MethodNode, self).__init__(text=text, metadata=metadata, id=id, node_relationships=node_relationships, node_type=node_type, file=file)


class ClassNode(BaseNode):
    
     def __init__(self, 
                  text: str, 
                  file: str, 
                  node_type: NodeType, 
                  metadata: Optional[Dict[str, Any]] | None = None, 
                  id: Optional[str] | None = None, 
                  node_relationships: Optional[Dict[NodeRelationshipType, Type['BaseNode']]] | None = None):
        
        super(ClassNode, self).__init__(text=text, metadata=metadata, id=id, node_relationships=node_relationships, node_type=node_type, file=file)

    
class CodeNode(BaseNode):
    
     def __init__(self, 
                  text: str, 
                  file: str, 
                  node_type: NodeType, 
                  metadata: Optional[Dict[str, Any]] | None = None, 
                  id: Optional[str] | None = None, 
                  node_relationships: Optional[Dict[NodeRelationshipType, Type['BaseNode']]] | None = None):
        
        super(CodeNode, self).__init__(text=text, metadata=metadata, id=id, node_relationships=node_relationships, node_type=node_type, file=file)
        
        
class ModuleNode(BaseNode):
    
     def __init__(self, 
                  text: str, 
                  file: str,
                  node_type: NodeType, 
                  metadata: Optional[Dict[str, Any]] | None = None, 
                  id: Optional[str] | None = None, 
                  node_relationships: Optional[Dict[NodeRelationshipType, Type['BaseNode']]] | None = None):
        
        super(ModuleNode, self).__init__(text=text, metadata=metadata, id=id, node_relationships=node_relationships, node_type=node_type, file=file)
