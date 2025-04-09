__version__ = "3.2.10"

# common
from .commons_pb2 import (
    InnerContextItem,
    ChatItem,
    ReplicaItem,
    OuterContextItem,
)

# Text
from .text_client import TextClient
from .DigitalAssistantText_pb2 import (
    DigitalAssistantTextRequest,
    DigitalAssistantTextResponse,
)
from .DigitalAssistantText_pb2_grpc import (
    DigitalAssistantText,
    DigitalAssistantTextServicer,
    DigitalAssistantTextStub,
    add_DigitalAssistantTextServicer_to_server,
)

# Critic
from .critic_client import CriticClient
from .DigitalAssistantCritic_pb2 import (
    DigitalAssistantCriticRequest,
    DigitalAssistantCriticResponse,
)
from .DigitalAssistantCritic_pb2_grpc import (
    DigitalAssistantCritic,
    DigitalAssistantCriticServicer,
    DigitalAssistantCriticStub,
    add_DigitalAssistantCriticServicer_to_server,
)

# ChatManager
from .chat_manager_client import ChatManagerClient
from .DigitalAssistantChatManager_pb2 import (
    DigitalAssistantChatManagerRequest,
    DigitalAssistantChatManagerResponse,
)
from .DigitalAssistantChatManager_pb2_grpc import (
    DigitalAssistantChatManager,
    DigitalAssistantChatManagerServicer,
    DigitalAssistantChatManagerStub,
    add_DigitalAssistantChatManagerServicer_to_server,
)

# OCR
from .ocr_client import OCRClient
from .ocr_enriched_client import OCREnrichedClient
from .DigitalAssistantOCR_pb2 import (
    OCRType,
    DigitalAssistantOCRRequest,
    DigitalAssistantOCRResponse,
)
from .DigitalAssistantOCR_pb2_grpc import (
    DigitalAssistantOCR,
    DigitalAssistantOCRServicer,
    DigitalAssistantOCRStub,
    add_DigitalAssistantOCRServicer_to_server,
)

# ContentRouter
from .content_router_client import ContentRouterClient
from .DigitalAssistantContentRouter_pb2 import (
    DigitalAssistantContentRouterRequest,
    DigitalAssistantContentRouterResponse,
)
from .DigitalAssistantContentRouter_pb2_grpc import (
    DigitalAssistantContentRouter,
    DigitalAssistantContentRouterServicer,
    DigitalAssistantContentRouterStub,
    add_DigitalAssistantContentRouterServicer_to_server,
)

# MedVersaModels
from .medversa_models_client import MedVersaModelsClient
from .DigitalAssistantMedVersaModels_pb2 import (
    DigitalAssistantMedVersaModelsRequest,
    DigitalAssistantMedVersaModelsResponse,
)
from .DigitalAssistantMedVersaModels_pb2_grpc import (
    DigitalAssistantMedVersaModels,
    DigitalAssistantMedVersaModelsServicer,
    DigitalAssistantMedVersaModelsStub,
    add_DigitalAssistantMedVersaModelsServicer_to_server,
)
