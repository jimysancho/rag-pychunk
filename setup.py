from setuptools import setup, find_packages

setup(
    name='rag-pychunk',
    version='1.0.4',
    packages=find_packages(),
    scripts=['scripts/python-scripts/classify-python-code.sh', 
             'scripts/python-scripts/find-node-relationships.sh', 
             'scripts/python-scripts/generate-node-metadata.sh'],
    author="Jaime Sancho Molero", 
    author_email="jimysanchomolero@gmail.com", 
    description="Improve your RAG pipelines for your python repositories.",
    long_description="""
    It leverages the python programming language syntax to improve: \n
    1. Chunk content \n
    2. Relationships between nodes \n
    
    \n
    The chunk size is dynamic: \n

    - The content of a function will be put together in the same chunk. \n
    - The content of a method will be put together in the same chunk. \n
    - Free code will be put together in the same chunk if it is found somewhere in the code. \n
    
    \n
    With code, the relationships parent - child and prev - next are not really usefull, because when defining big projects, there is no particular order in the code itself, so prev-next does not really make sense (only when the definition of the code is really large, for example a big function or big class). It is much more important to know: \n

    If a function in a file X is called in a file Y, when the function of file Y is retrieved the function of file X should be retrieved as well so that the LLM has the complete picture of file Y. \n
    If a method in some class is called somewhere else in the class, it should be noted as well. \n
    These are the kind of relationships that can be obtained to improve the context feeding part for the LLM. \n
    """
)
