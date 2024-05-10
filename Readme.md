# Description

Python Library to chunk your python files levereging the python programming language to leverage two things: 
1. Chunk size: make your chunk size dynamic, keeping in the same chunk a hole funcion, a hole class method, a hole class and block of code. 
2. Chunk relationships: create relationships between your chunks other than `Parent-Child` and `Prev-Next`. 

# How to use it

```
from pychunk.chunkers.python_chunker import PythonChunker

files_path = ["your python file/directory here!"]
chunker = PythonChunker(files_path=files_path)

nodes = chunker.find_relationships()
```

Enjoy your relationships! 

# Other repositories

- https://github.com/jimysancho/python-gpt. Chat with your python repository by levering the relationships and chunk size. 
