import pickle

class Document:

    def init(self, req_type: str=None, payload: list=None) -> None:
        """
        Creates a document, as a method of communication.

        Args:
            req_type (str, optional): Type of request. Defaults to None.
            payload (list, optional): Payload of response. Defaults to None.
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
        Serializes a document.

        Returns:
            bytes: serialized self
        """
        return pickle.dumps(self)

    def str(self) -> str:
        """
        When printing docs, str will be called and return a comfortable string.

        Returns:
            str: represenation of the document.
        """
        return f'Document: type = {self.type}\n' + f'paylod = {self.payload}'