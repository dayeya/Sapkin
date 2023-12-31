import pickle
from typing import Any, Self

class Document:

    def __init__(self, req_type: str = "MSG", payload: Any = None) -> None:
        """
        Document object.
        :param req_type: Defaults to none
        :param payload: Defaults to none
        """
        self._type = req_type
        self._payload = payload

    @property
    def type(self) -> str:
        """
        Getter for _type
        :return: type of self
        """
        return self._type

    @property
    def payload(self) -> Any:
        """
        Getter for _payload
        :return: payload of self
        """
        return self._payload
    
    def __enter__(self) -> Any:
        return self.payload
    
    def __exit__(self, type, value, tracebeck) -> None:
        del self

    def serialize(self) -> bytes:
        """
        Serializes self into bytes.
        :return: bytes of self
        """
        return pickle.dumps(self)

    def __str__(self) -> str:
        """
        Useful for debugging.
        :return: str representation of self
        """
        return f'Document: type = {self.type}\n' + f'payload = {self.payload}'

