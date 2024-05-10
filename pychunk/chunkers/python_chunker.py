from pychunk.chunkers.base import Chunker
from pychunk.nodes.base import BaseNode
from pychunk.nodes.nodes import ClassNode, FunctionNode, CodeNode, MethodNode, ModuleNode
from pychunk.nodes.types import NodeType, NodeMetadata, NodeRelationshipType
from pychunk.utils.nodes_utils import create_nodes_from_file

from typing import (List,
                    Callable, 
                    Optional, 
                    Dict, 
                    Type)

import subprocess
import os
import re


class PythonChunker(Chunker):
    
    _node_type_to_node_base: Dict[NodeType, Type['BaseNode']] = {
        NodeType.CLASS: ClassNode, 
        NodeType.CODE: CodeNode, 
        NodeType.FUNCTION: FunctionNode, 
        NodeType.METHOD: MethodNode, 
        NodeType.MODULE: ModuleNode
    }
    
    _not_valid_relationships_to_look_pattern = r"^__[^_]*__$"
    
    def __init__(self, files_path: str | List[str], hash_function: Optional[Callable] | None = None):
        super(PythonChunker, self).__init__(files_path=files_path, hash_function=hash_function)
        
    def _create_nodes_of_file(self, file_path: str) -> Dict[str, Type['BaseNode']]:
        
        tmp_folder = self._file_handler.tmp_folder
        if file_path.startswith("."): file_path = file_path[2:]
        elif file_path.startswith(".."): file_path = file_path[3:]
        file_name = file_path.replace("/", "_").split(".")[0]
        command = f"./scripts/python-scripts/generate-node-metadata.sh {file_path} {tmp_folder}/{file_name}_info.txt > {tmp_folder}/{file_name}_final.txt 2> /dev/null"
        subprocess.run(["bash", "-c", command])

        nodes = {}
        hashes = set()
        classes_names_to_uuids = {}
                
        for (code, lines_of_code, class_name, function_or_method_name, node_type, metadata) in create_nodes_from_file(f"{tmp_folder}/{file_name}_final.txt"):
            if code is None or lines_of_code is None:
                continue
            remove_commas_spaces_and_new_lines = code.replace(",", "").replace("\n", "").strip().replace(" ", "")
            try:
                int(remove_commas_spaces_and_new_lines)
                continue
            except Exception:
                pass
                        
            hash = self._hash_function(text=code)
            if hash in hashes: continue
            hashes.add(hash)
            node_class = self._node_type_to_node_base[node_type]
            node_object = node_class(
                text=code,
                node_type=node_type, 
                file=file_path
            )
            
            if node_type == NodeType.CLASS:
                classes_names_to_uuids[class_name.replace(" ", "")] = node_object.id
                uuid_of_parent_node = None
                node_metadata = NodeMetadata(
                    hash=hash, 
                    lines_of_code=lines_of_code, 
                    additional_metadata={'parent_class': metadata.strip(), 'class_name': class_name.strip()}
                )
                node_object.metadata = node_metadata.model_dump()
                nodes[node_object.id] = node_object
                
            elif node_type == NodeType.METHOD:
                uuid_of_parent_node = classes_names_to_uuids[class_name.replace(" ", "")]
                parent_node = nodes[uuid_of_parent_node]
                node_metadata = NodeMetadata(
                    hash=hash, 
                    lines_of_code=lines_of_code, 
                    additional_metadata={'arguments': metadata.strip(), 'method_name': function_or_method_name.strip()} 
                )
                node_object.metadata = node_metadata.model_dump()
                node_object.add_relationship(parent_node, relationship_type=NodeRelationshipType.PARENT)
                parent_node.add_relationship(node_object, relationship_type=NodeRelationshipType.CHILD)
                nodes[node_object.id] = node_object
                
            elif node_type == NodeType.FUNCTION:
                
                node_metadata = NodeMetadata(
                    hash=hash, lines_of_code=lines_of_code, additional_metadata={'arguments': metadata.strip(), 'function_name': function_or_method_name.strip()}
                )
                node_object.metadata = node_metadata.model_dump()
                nodes[node_object.id] = node_object
                
            elif node_type == NodeType.CODE:
                node_metadata = NodeMetadata(
                    hash=hash, lines_of_code=lines_of_code, additional_metadata=metadata if metadata else {}
                )
                node_object.metadata = node_metadata.model_dump()
                nodes[node_object.id] = node_object
                
            elif node_type == NodeType.MODULE:
                node_metadata = NodeMetadata(
                    hash=hash, 
                    lines_of_code=lines_of_code, 
                    additional_metadata={'modules': metadata if metadata else {}}
                )
                node_object.metadata = node_metadata.model_dump()
                nodes[node_object.id] = node_object
        
        return nodes
            
    def _create_nodes(self) -> Dict[str, Dict[str, Type['BaseNode']]]:
        nodes = {}
        for file in self._files_path:
            try:
                nodes[file] = self._create_nodes_of_file(file_path=file)
            except Exception as e:
                self._file_handler.delete_tmp_folder()
                raise e
        return nodes
    
    def find_relationships(self) -> Dict[str, Dict[str, Type['BaseNode']]]:
        try:
            return self._create_relationships_of_nodes()
        except Exception as e:
            self._file_handler.delete_tmp_folder()
            raise e
            
    def _create_relationships_of_nodes(self) -> Dict[str, Dict[str, Type['BaseNode']]]:
        
        nodes_of_files_dict = self._create_nodes()
        nodes_of_files = []
        for _, nodes_file in nodes_of_files_dict.items():
            nodes_of_files.extend(list(nodes_file.values()))

        tmp_folder = self._file_handler.tmp_folder
        
        fields = ('class_name', 'function_name', 'method_name')
        name_file = os.path.join(tmp_folder, "names.txt")
        relationships_file = os.path.join(tmp_folder, "node_relationships.txt")
            
        nodes = []
        with open(name_file, "w") as names_file:
            for field in fields:
                get_nodes_of_field = lambda n: [x for x in n if x.metadata['additional_metadata'].get(field) is not None]
                nodes_of_field = get_nodes_of_field(nodes_of_files)
                nodes.extend(nodes_of_field)
            for node in nodes:
                node_metadata = node.metadata['additional_metadata']
                for field in fields:
                    name = node_metadata.get(field)
                    if name is None or re.match(self._not_valid_relationships_to_look_pattern, name): continue
                    names_file.write(f"{name} {node.id} {node.file}\n")
        
        for path in self._files_path:    
            command = f"./scripts/python-scripts/find-node-relationships.sh {name_file} {path} >> {relationships_file} 2> /dev/null" 
            subprocess.run(["bash", "-c", command])
           
        with open(relationships_file, "r") as node_relationship_file:
            lines = node_relationship_file.readlines()
                                    
        start = False 
        get_node = lambda id_: [node for node in nodes_of_files if node.id == id_]
        for line in lines:
            if line.startswith("#- BEGIN"): 

                start = True
                node_id = line.split(" ")[-2].strip()
                
            elif line.startswith("#- END"): 
                start = False
                
            if start:
                parts = line.split(":")[-1].split("-")
                if len(parts) > 2:
                    file_path = "-".join(parts[:-1]).strip()
                    line_of_code = parts[-1].strip()
                else:
                    file_path, line_of_code = line.split(":")[-1].split("-")[0].strip(), line.split(":")[-1].split("-")[-1].strip()
                if "#" in file_path: continue
                nodes_of_file = nodes_of_files_dict[file_path]
                node_relationship_with, = get_node(node_id)
                                                   
                for node in nodes_of_file.values():
                    
                    lines_of_code = node.metadata.get('lines_of_code')
                    is_node_relationsihp_with_its_child_node = node.check_relationship(node_relationship_with, relationship_type=NodeRelationshipType.CHILD)
                                    
                    if lines_of_code is None or node == node_relationship_with or is_node_relationsihp_with_its_child_node: continue
                    
                    if int(lines_of_code[0]) <= int(line_of_code) <= int(lines_of_code[1]):
                        node.add_relationship(node_relationship_with, NodeRelationshipType.OTHER, line_of_code)
        
        self._file_handler.delete_tmp_folder()
        return nodes_of_files_dict
