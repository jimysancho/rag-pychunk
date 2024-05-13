from pychunk.nodes.types import NodeType

from typing import Generator, Tuple

class Pointer: 
    start = 'start'
    end = 'end'

class Delimiter:

    module_delimiter = {Pointer.start: "#- BEGIN MODULES -#", Pointer.end: "#- END MODULES -#"}
    function_delimiter = {Pointer.start: "#- BEGIN FUNCTION", Pointer.end: "#- END FUNCTION"}
    class_delimiter = {Pointer.start: "#- BEGIN CLASS", Pointer.end: "#- END CLASS"}
    method_delimiter = {Pointer.start: "#- BEGIN METHOD OF CLASS", Pointer.end: "#- END METHOD OF CLASS"}
    free_code_delimiter = {Pointer.start: "#- BEGIN BLOCK OF CODE -#", Pointer.end: "#- END BLOCK OF CODE -#"}

def create_nodes_from_file(file: str) -> Generator[Tuple, None, None]:
    lines = open(file).readlines()
    modules_text = None 
    class_text = None 
    method_text = None 
    function_text = None 
    free_code = None 
    
    # TODO -> refactor this into smaller functions
        
    for line in lines:
                                        
        if line.startswith(Delimiter.module_delimiter[Pointer.start]):
            modules_text = []
            class_text = None
            function_text = None 
            method_text = None 
            free_code = None 
            
            begin_module_line = True  
            end_module_line = False 
        
        elif line.startswith(Delimiter.class_delimiter[Pointer.start]):
            class_text = []
            modules_text = None
            function_text = None 
            method_text = None 
            free_code = None 
            
            begin_class_line = True  
            end_class_line = False 
            class_name = line.replace(" ", "").split(":")[-1][:-3]
            
        
        elif line.startswith(Delimiter.function_delimiter[Pointer.start]):

            function_text = []
            method_text = None 
            class_text = None 
            modules_text = None 
            free_code = None 
            
            begin_function_line = True 
            end_function_line = False 
            
        elif line.startswith(Delimiter.free_code_delimiter[Pointer.start]):
            
            free_code = []
            function_text = None
            method_text = None 
            class_text = None 
            modules_text = None 
            
            begin_free_code = True 
            end_free_code = False 
    
        elif line.startswith(Delimiter.module_delimiter[Pointer.end]) and isinstance(modules_text, list):
            modules_content = "".join(modules_text)
            modules_text = None 
            end_module_line = True 
            yield modules_content, None , None, None, NodeType.MODULE, None
            
        elif line.startswith(Delimiter.class_delimiter[Pointer.end]) and isinstance(class_text, list):
            class_metadata = class_text[0].split(":")[-1]

            try:
                begin_line, end_line = class_metadata.split("-")[-1].split(",")
                begin_line = begin_line.replace("\n", "")
                end_line = end_line.replace("\n", "")
                if not len(end_line.strip()):
                    end_line = int(begin_line) + 1
            except ValueError:
                begin_line = class_metadata.split("-")[-1].split(",")[0]
                end_line = int(begin_line) + 1
                            
            metadata = class_metadata.split(":")[-1].split("-")[0]
            del class_text[0]
            class_content = "".join(class_text)
            class_text = None 
            end_class_line = True 
            begin_class_line = False 
            try:
                yield class_content, (int(begin_line), int(end_line)), class_name, None, NodeType.CLASS, metadata
            except:
                yield class_content, None, class_name, None, NodeType.CLASS, metadata
                            
        elif line.startswith(Delimiter.function_delimiter[Pointer.end]) and isinstance(function_text, list):

            end_function_line = True 
            begin_function_line = False 
            function_metadata = function_text[0]
            metadata = function_text[0].split("Arguments:")[-1].split("-")[0]
            function_name = line.split("FUNCTION:")[-1].replace(" ", "")[:-3]
            try:
                begin_line, end_line = function_metadata.split("-")[-1].split(",")
            except Exception as e:
                begin_line, end_line = None, None
                
            if not len(end_line.strip()): end_line = int(begin_line) + 1
            del function_text[0]
            function_content = "".join(function_text)
            function_text = None 
            try:
                yield (function_content, 
                    (int(begin_line), 
                    int(end_line)), 
                    None, 
                    function_name, 
                    NodeType.FUNCTION, 
                    metadata)
            except Exception as e:
                yield (function_content, None, None, function_name, NodeType.FUNCTION, metadata)
            
        elif line.startswith(Delimiter.free_code_delimiter[Pointer.end]) and isinstance(free_code, list):
            end_free_code = True 
            begin_free_code = False 
            code_metadata = free_code[0]
            try:
                begin_line, end_line = code_metadata.split(":")[-1].split(",")
            except Exception as e:
                begin_line = None
                end_line = None
                
            del free_code[0]
            code_content = "".join(free_code)
            free_code = None 
            try:
                yield (code_content, 
                    (int(begin_line), 
                    int(end_line)), 
                    None, 
                    None, 
                    NodeType.CODE, 
                    None)
            except Exception as e:
                yield (code_content, None, None, None, NodeType.CODE, None)
            
        if isinstance(modules_text, list):
            if begin_module_line: 
                begin_module_line = False 
                continue
            if end_module_line:
                continue
            
            modules_text.append(line)
            
        elif isinstance(class_text, list):
            if begin_class_line: 
                begin_class_line = False 
                continue
            if end_class_line:
                continue
            class_text.append(line)
                
        elif isinstance(function_text, list):
            if begin_function_line:
                begin_function_line = False 
                continue
            if end_function_line:
                continue
            function_text.append(line)

        elif isinstance(free_code, list):
            if begin_free_code:
                begin_free_code = False 
                continue
            if end_free_code:
                continue
            free_code.append(line)
            

    for line in lines:
                    
        if line.startswith(Delimiter.method_delimiter[Pointer.start]):
            method_text = []
            class_text = None 
            modules_text = None
            function_text = None 
            free_code = None 
            
            begin_method_line = True 
            end_method_line = False 
            
        elif line.startswith(Delimiter.method_delimiter[Pointer.end]) and isinstance(method_text, list):
            method_metadata = method_text[0]
            metadata = method_metadata.split("Arguments:")[-1].split("-")[0]
            class_name = line.split("CLASS")[-1].split(":")[0].replace(" ", "")
            method_name = line.split("CLASS")[-1].split(":")[1].replace(" ", "")[:-3]
            begin_line, end_line = method_metadata.split("-")[-1].split(",")
            del method_text[0]
            method_content = "".join(method_text)
            method_text = None 
            end_method_line = True 
            begin_method_line = False 

            try:
                yield (method_content, 
                      (int(begin_line), 
                       int(end_line)), 
                       class_name, 
                       method_name, 
                       NodeType.METHOD, 
                       metadata)
            except Exception as e:
                yield (method_content, None, class_name, method_name, NodeType.METHOD, metadata)
            
        if isinstance(method_text, list):
            if begin_method_line: 
                begin_method_line = False 
                continue
            if end_method_line:
                continue
            method_text.append(line)
            
