import pickle

class Document:
    
    def __init__(self, req_type: str=None, payload: list=None) -> None:
        """
        Creates a doc object.

        Args:
            req_type (str): request type for server.
        """
        self._type = req_type
        self._payload = payload
    
    @property
    def type(self) -> str:
        """
        Returns:
            str: type if there is one, else None.
        """
        return self._type
    
    @property
    def payload(self) -> list:
        """
        Returns:
            list: payload if there is one, else None.
        """
        return self._payload
    
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
        return f'Document: type = {self.type}\n' + f'paylod = {self.payload}'
