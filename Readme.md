# Description

Python Library to chunk your python files levereging the python programming language to leverage two things: 
1. Chunk size: make your chunk size dynamic, keeping in the same chunk a hole funcion, a hole class method, a hole class and block of code. 
2. Chunk relationships: create relationships between your chunks other than `Parent-Child` and `Prev-Next`. 

# How to use it

First install it via *pip* command: 
```
pip install rag-pychunk
```

```
from pychunk.chunkers.python_chunker import PythonChunker

files_path = ["your python file/directory here!"]
chunker = PythonChunker(files_path=files_path)

nodes = chunker.find_relationships()
```
### Basic Entities

1. **NodeType**

It encapsulates the different types of nodes: *method*, *class*, *function*, *free block of code*, *module imports*
```
class NodeType(Enum):
    
    MODULE = "MODULE" 
    METHOD = "METHOD"
    CLASS = "CLASS"
    FUNCTION = "FUNCTION"
    CODE = "CODE"
    
```

2. **NodeRelationshipType**

It describes the different types of relationships that may exist between the nodes: 
- *Parent - Child*: a class' method. 
- *Prev - Next*: the order in which the nodes appear (not used for the moment). 
- *Other*: when a node is called in another node (a method inside another method, a function somewhere in the code, etc).
```
class NodeRelationshipType(Enum): 
    
    PARENT = "PARENT"
    CHILD = "CHILD"
    PREV = "PREV"
    NEXT = "NEXT"
    OTHER = "OTHER"
    SELF = "SELF"
```

3. **NodeMetadata**

Pydantic model to store the node metadata more easily. Then is passed as a dictionary to the BaseNode object. 
```
class NodeMetadata(BaseModel):
    
    hash: str
    lines_of_code: Tuple[int, int] | None
    additional_metadata: Optional[Dict[Any, Any]] | None = None
```

4. **BaseNode**

In the file: https://github.com/jimysancho/rag-pychunk/blob/main/pychunk/nodes/base.py there is the BaseNode definition.
```
class BaseNode(ABC):
    
    def __init__(self, 
                 text: str, 
                 file: str, 
                 node_type: NodeType, 
                 metadata: Optional[Dict[str, Any]] | None = None, 
                 id: Optional[str] | None = None, 
                 node_relationships: Optional[Dict[str, List[Tuple[Type['BaseNode'], int | None]]]] | None = None):
        
        if not isinstance(node_type, NodeType):
            raise TypeError(f"Argument node_type must be NodeType. Right now is: {type(node_type)}")
        
        self.__uuid = id if id else str(uuid.uuid4())
        self._text = text
        self._file = file
        self._type = node_type
        self.__node_relationships = {} if node_relationships is None else node_relationships
        self._metadata = {} if metadata is None else metadata
```

### Filter relationships

Using filter_relationship method you can get all of the relationships of a given node that are of the type: `relationship_type`.  
```
  def filter_relationships(self, relationship_type: NodeRelationshipType) -> List[Tuple[Type['BaseNode'], int | None]] | List:
        relationship_type = relationship_type.value
        filtered_relationships = [rel for rel_type, rel in self.__node_relationships.items() if rel_type == relationship_type]
        if len(filtered_relationships) > 0:
            return filtered_relationships[0]
        return []
```

# Integrations

You can use the `LlamaIndexParser` and `LangChainParser` to transform the nodes in compatible objects with these frameworks: 

- **LlamaIndex**
```
from pychunk.parser.llama_index_parser import LlamaIndexParser

llama_index_parser = LlamaIndexParser(nodes=list(all_nodes.values()))
llama_index_nodes = llama_index_parser.parse_to_llama_index()

```

- **Langchain**
```
from pychunk.parser.langchain_parser import LangChainParser

langchain_parser = LangChainParser(nodes=list(all_nodes.values()))
documents = langchain_parser.parse_to_langchain_document()
```

# Other repositories

- https://github.com/jimysancho/python-gpt. Chat with your python repository by levering the relationships and chunk size. 
