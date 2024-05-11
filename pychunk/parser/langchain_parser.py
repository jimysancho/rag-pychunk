try:
    from langchain_community.docstore.document import Document
except ModuleNotFoundError:
    raise ModuleNotFoundError("You need to install langchain. Run: pip install langchain")

from pychunk.nodes.base import BaseNode, NodeRelationshipType
from typing import List, Dict, Any

from pydantic import BaseModel

class NodeMetadata(BaseModel):
    
    child_relationships: List[str]
    parent_relationships: List[str]
    other_relationships: List[str]
    additional_metadata: Dict[str, Any]

class LangChainParser:
    
    def __init__(self, nodes: BaseNode | List[BaseNode]): 
        if not isinstance(nodes, list):
            nodes = [nodes]
        self._nodes = nodes
        
    def parse_to_langchain_documents(self) -> List[Document]:
        documents = []
        for node in self._nodes:
            document = Document(page_content=node.content, metadata=self._create_metadata_from_node(node))
            documents.append(document)
            
        return documents
        
    def _create_metadata_from_node(self, node: BaseNode) -> Dict[str, Any]:
        metadata = node.metadata
        additional_metadata = {'relationships': []}
        if node.relationships:
            for relationship_type, relationships in node.relationships.items():
                for relation_id in relationships:
                    additional_metadata['relationships'].append(relation_id)
                    
        metadata = {**metadata, **additional_metadata}
        return metadata
        