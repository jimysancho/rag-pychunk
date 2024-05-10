from enum import Enum
try:
    from pydantic import BaseModel
except ModuleNotFoundError:
    raise ModuleNotFoundError("You need to install pydantic in order to use this library")

from typing import (
    Optional, 
    Any, 
    List, 
    Tuple, 
    Dict
)

class NodeType(Enum):
    
    MODULE = "MODULE"
    METHOD = "METHOD"
    CLASS = "CLASS"
    FUNCTION = "FUNCTION"
    CODE = "CODE"
    
    
class NodeRelationshipType(Enum): 
    
    PARENT = "PARENT"
    CHILD = "CHILD"
    PREV = "PREV"
    NEXT = "NEXT"
    OTHER = "OTHER"
    SELF = "SELF"
    

class FileType(Enum): 
    
    PYTHON = "PYTHON"
    
class NodeMetadata(BaseModel):
    
    hash: str
    lines_of_code: Tuple[int, int] | None
    additional_metadata: Optional[Dict[Any, Any]] | None = None