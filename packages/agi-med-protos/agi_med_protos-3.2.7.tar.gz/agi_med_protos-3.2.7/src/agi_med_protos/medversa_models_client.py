from .commons_pb2 import OuterContextItem
from .DigitalAssistantMedVersaModels_pb2_grpc import DigitalAssistantMedVersaModelsStub
from .DigitalAssistantMedVersaModels_pb2 import (
    DigitalAssistantMedVersaModelsRequest,
    DigitalAssistantMedVersaModelsResponse,
)
from .abstract_client import AbstractClient


class MedVersaModelsClient(AbstractClient):
    def __init__(self, address):
        super().__init__(address)
        self._stub = DigitalAssistantMedVersaModelsStub(self._channel)

    def interpret(
        self,
        outer_context: OuterContextItem,
        resource_id: str = None,
        resource: bytes = None,
        request_id: str = "",
    ) -> DigitalAssistantMedVersaModelsResponse:
        if resource is None and resource_id is None:
            raise ValueError("Argument `resource` or `resource_id` should be passed!")
        request = DigitalAssistantMedVersaModelsRequest(
            OuterContext=outer_context,
            ResourceId=resource_id,
            Image=resource,
            RequestId=request_id,
        )
        response: DigitalAssistantMedVersaModelsResponse = self._stub.Interpret(request)
        return response
