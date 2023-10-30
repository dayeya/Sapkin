import pickle


class Document:
    
    def __init__(self, req_type: str) -> None:
        """
        Creates a Doc object.

        Args:
            req_type (str): request type for server.
        """
        self.doc = { "type": req_type }
        
    def serialize(self) -> bytes:
        """
        Returns serialized representation of the document.

        Returns:
            bytes: serialized 'seld.doc'
        """
        return pickle.dumps(
            self.doc
        )
        
    def serialize(self) -> bytes:
        """
        Returns serialized representation of the document.

        Returns:
            bytes: serialized 'seld.doc'
        """
        return pickle.loads(
            self.doc
        )
