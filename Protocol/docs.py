import pickle

class Document:
    
    TYPE = 'type'
    PAYLOAD = 'payload'
    
    def __init__(self, req_type: str, payload: str=None) -> None:
        """
        Creates a doc object.

        Args:
            req_type (str): request type for server.
        """
        self.doc = {"rtype": req_type, **({"payload": payload} if payload else {})}
        
    def serialize(self) -> bytes:
        """
        Serializes 'self'.

        Returns:
            bytes: serialized 'self.doc'
        """
        return pickle.dumps(self)
        
    def __str__(self) -> str:
        """
        When printing docs, __str__ will be called and return a comfortable string.

        Returns:
            str: represenation of the document.
        """
        return f'Document: type = {self.doc[Document.TYPE]}\n' + f'paylod = {self.doc[Document.PAYLOAD]}'