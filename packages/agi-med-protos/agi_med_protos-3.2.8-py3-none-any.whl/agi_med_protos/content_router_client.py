from typing import Tuple

from .commons_pb2 import (
    OuterContextItem,
)
from .DigitalAssistantContentRouter_pb2_grpc import DigitalAssistantContentRouterStub
from .DigitalAssistantContentRouter_pb2 import (
    DigitalAssistantContentRouterRequest,
    DigitalAssistantContentRouterResponse,
)
from .abstract_client import AbstractClient
from .converters import convert_outer_context

ResourceId = str
Interpretation = str

class ContentRouterClient(AbstractClient):
    def __init__(self, address):
        super().__init__(address)
        self._stub = DigitalAssistantContentRouterStub(self._channel)

    def interpret(
        self, resource_id: str, prompt: str, dict_outer_context: dict, request_id: str = ""
    ) -> Tuple[Interpretation, ResourceId]:
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

        request = DigitalAssistantContentRouterRequest(
            RequestId=request_id,
            OuterContext=outer_context,
            ResourceId=resource_id,
            Prompt=prompt,
        )
        response: DigitalAssistantContentRouterResponse = self._stub.Interpret(request)
        return response.Interpretation, response.ResourceId
