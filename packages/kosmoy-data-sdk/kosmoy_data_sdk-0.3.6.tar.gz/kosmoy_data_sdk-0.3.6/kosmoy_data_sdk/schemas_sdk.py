from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


# Base models for common fields
class BaseSdkModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    id: int


class NameDescriptionModel(BaseSdkModel):
    name: str
    description: Optional[str] = None


# User Status
class UserStatusModel(BaseSdkModel):
    name: str


# Assistant Types
class AssistantTypesModel(NameDescriptionModel):
    pass


# Assistant Scopes
class AssistantScopesModel(BaseSdkModel):
    name: str


# Service Types
class ServiceTypesModel(NameDescriptionModel):
    pass


# Services
class ServicesModel(NameDescriptionModel):
    provider_id: int
    service_type_id: int
    req_config_params: Optional[Dict[str, Any]] = None


# Data Source Types
class DataSourceTypesModel(NameDescriptionModel):
    pass


# Data Sources
class DataSourcesModel(NameDescriptionModel):
    provider_id: int
    data_source_type_id: int
    req_config_params: Optional[Dict[str, Any]] = None


# Channels
class ChannelsModel(NameDescriptionModel):
    assistant_scope_id: int
    provider_id: int
    req_config_params: Optional[Dict[str, Any]] = None


# Assistant Types Service Types
class AssistantTypesServiceTypesModel(BaseSdkModel):
    assistant_type_id: int
    service_type_id: int


# Session Types
class SessionTypesModel(BaseSdkModel):
    name: str


# Connection Types
class ConnectionTypesModel(NameDescriptionModel):
    pass


# Connection Providers
class ConnectionProvidersModel(NameDescriptionModel):
    connection_type_id: int
    req_connection_params: Dict[str, Any]
    req_collection_params: Optional[Dict[str, Any]] = None


# Vector Distance Strategies
class VectorDistanceStrategiesModel(NameDescriptionModel):
    pass


# Connection Providers Vector Distance Strategies
class ConnectionProvidersVectorDistanceStrategiesModel(BaseSdkModel):
    connection_provider_id: int
    vector_distance_strategy_id: int


# Retriever Types
class RetrieverTypesModel(NameDescriptionModel):
    pass


# Retriever Strategies
class RetrieverStrategiesModel(NameDescriptionModel):
    req_retriever_params: Dict[str, Any]


# Vector Channel Strategies
class VectorChannelStrategiesModel(NameDescriptionModel):
    req_vector_channel_params: Optional[Dict[str, Any]] = None


# Run Statuses
class RunStatusesModel(BaseSdkModel):
    name: str


# Avatars
class AvatarsModel(BaseSdkModel):
    avatar_path: str
    is_default: bool = True


# Guardrail Types
class GuardrailTypesModel(NameDescriptionModel):
    allowed_scopes: List[str]
    allowed_subtypes: Optional[List[str]] = None
    is_built_in: bool = False


# List response models
class UserStatusListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[UserStatusModel]


class AssistantTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[AssistantTypesModel]


class AssistantScopesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[AssistantScopesModel]


class ServiceTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[ServiceTypesModel]


class ServicesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[ServicesModel]


class DataSourceTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[DataSourceTypesModel]


class DataSourcesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[DataSourcesModel]


class ChannelsListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[ChannelsModel]


class AssistantTypesServiceTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[AssistantTypesServiceTypesModel]


class SessionTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[SessionTypesModel]


class ConnectionTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[ConnectionTypesModel]


class ConnectionProvidersListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[ConnectionProvidersModel]


class VectorDistanceStrategiesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[VectorDistanceStrategiesModel]


class ConnectionProvidersVectorDistanceStrategiesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[ConnectionProvidersVectorDistanceStrategiesModel]


class RetrieverTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[RetrieverTypesModel]


class RetrieverStrategiesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[RetrieverStrategiesModel]


class VectorChannelStrategiesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[VectorChannelStrategiesModel]


class RunStatusesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[RunStatusesModel]


class AvatarsListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[AvatarsModel]


class GuardrailTypesListModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    items: List[GuardrailTypesModel]


# Original fixed data models (keeping for backward compatibility)
class ProviderModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    id: int
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None
    req_config_params: Optional[Dict[str, Any]] = None
    stage_name: str = "development"


class ModelCreatorModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    id: int
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None
    stage_name: str = "development"


class ModelTypeModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    id: int
    name: str
    description: Optional[str] = None
    stage_name: str = "development"


class AvailableModelModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    id: int
    provider: ProviderModel
    creator: ModelCreatorModel
    model_type: ModelTypeModel
    name: str
    model_id: str
    req_config_params: Optional[Dict[str, Any]] = None
    cost_input_token: float
    cost_output_token: float
    embedding_dimension: Optional[int] = None
    is_verified: bool
    is_legacy: bool = False
    model_source_url: Optional[str] = None
    model_input: List[str]
    model_output: List[str]
    stage_name: str = "development"
