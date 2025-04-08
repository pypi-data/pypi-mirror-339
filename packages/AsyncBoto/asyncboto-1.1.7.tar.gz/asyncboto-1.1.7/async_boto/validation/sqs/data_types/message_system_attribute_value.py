from pydantic import BaseModel


class MessageSystemAttributeValue(BaseModel):
    """
    The user-specified message system attribute value. For string data types, the Value
    attribute has the same restrictions on the content as the message body.

    Attributes
    ----------
    DataType : str
        Amazon SQS supports the following logical data types: String, Number, and
        Binary. For the Number data type, you must use StringValue.
    BinaryListValues : Optional[List[bytes]]
        Not implemented. Reserved for future use.
    BinaryValue : Optional[bytes]
        Binary type attributes can store any binary data, such as compressed data,
        encrypted data, or images.
    StringListValues : Optional[List[str]]
        Not implemented. Reserved for future use.
    StringValue : Optional[str]
        Strings are Unicode with UTF-8 binary encoding.
    """

    DataType: str
    BinaryListValues: list[bytes] | None = None
    BinaryValue: bytes | None = None
    StringListValues: list[str] | None = None
    StringValue: str | None = None
