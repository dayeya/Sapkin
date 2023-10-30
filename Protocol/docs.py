import pickle


class Document:
    
    def __init__(self, req_type: str, payload: str=None) -> None:
        """
        Creates a Doc object.

        Args:
            req_type (str): request type for server.
        """
        self.doc = {"type": req_type, **({"payload": payload} if payload else {})}
        
    def serialize(self) -> bytes:
        """
        Returns serialized represenation of the document.

        Returns:
            bytes: serialized 'self.doc'
        """
        return pickle.dumps(
            self
        )
        
    def deserialize(self) -> bytes:
        """
        Returns serialized represenation of the document.

        Returns:
            bytes: deserialized 'self.doc'
        """
        return pickle.loads(
            self
        )