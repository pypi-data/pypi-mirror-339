from .abstract_client import AbstractClient
from .DigitalAssistantOCR_pb2 import (
    OCRType,
    DigitalAssistantOCRRequest,
    DigitalAssistantOCRResponse,
)
from .DigitalAssistantOCR_pb2_grpc import DigitalAssistantOCRStub


class OCRClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantOCRStub(self._channel)

    def __call__(
        self, document: bytes, ocr_type_: OCRType, request_id: str = ""
    ) -> str:
        request = DigitalAssistantOCRRequest(
            Document=document, OCRType=ocr_type_, RequestId=request_id
        )
        response: DigitalAssistantOCRResponse = self._stub.GetTextResponse(request)
        return response.Text
