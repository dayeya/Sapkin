import pickle

class Document:
    
    TYPE = 'rtype'
    PAYLOAD = 'payload'
    
    def __init__(self, req_type: str, payload: list=None) -> None:
        """
        Creates a doc object.

        Args:
            req_type (str): request type for server.
        """
        self.type = {"rtype": req_type, **({"payload": payload} if payload else {})}
    
    def get_type(self) -> str:
        """
        Returns:
            str: selfs type.
        """
        return self.type
    
    def get_payload(self) -> list:
        """
        Returns:
            str: selfs payload if there exists.
        """
        return self.payload
    
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
        return f'Document: type = {self.get_type()}\n' + f'paylod = {self.get_payload()}'
