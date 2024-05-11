try:
    from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo
except ModuleNotFoundError:
    raise ModuleNotFoundError("You need to install llama_index first. Run: pip install llama-index-core")

from pychunk.nodes.base import BaseNode, NodeRelationshipType
from typing import List, Dict

  
class LlamaIndexParser:
    
    def __init__(self, nodes: BaseNode | List[BaseNode]): 
        if not isinstance(nodes, list):
            nodes = [nodes]
        self._nodes = nodes
        
    def parse_to_llama_index(self) -> List[TextNode]:
        llama_index_nodes = []
        for node in self._nodes:
            llama_index_nodes.append(self._parse_relationship_to_llama_index(node=node))
        return llama_index_nodes
    
    @staticmethod
    def _parse_relationship_to_llama_index(node: BaseNode) -> TextNode:
        
        other_relationships = node.filter_relationships(NodeRelationshipType.OTHER)
        llama_index_node = None
        extra_info = node.metadata
        if len(other_relationships) > 0:
            relationships = []
            for other_node in other_relationships:
                relationships.append(other_node)
            extra_info['other_relationships'] = relationships.copy()
            llama_index_node = TextNode(id_=node.id, text=node.content, extra_info=extra_info)
    
        llama_index_node = TextNode(id_=node.id, text=node.content, extra_info=extra_info) if llama_index_node is None else llama_index_node
        relationships_child = node.filter_relationships(NodeRelationshipType.CHILD)
        if len(relationships_child) > 0:
            llama_index_node.relationships[NodeRelationship.CHILD] = []
            for child in relationships_child:
                llama_index_node.relationships[NodeRelationship.CHILD].append(RelatedNodeInfo(node_id=child))
        relationships_parent = node.filter_relationships(NodeRelationshipType.PARENT)
        if len(relationships_parent) > 0:
            parent, = list(relationships_parent.keys())
            llama_index_node.relationships[NodeRelationship.PARENT] = RelatedNodeInfo(node_id=parent)
        
        return llama_index_node