import requests
from typing import List, Optional
from pydantic import TypeAdapter
from schemas_sdk import (
    AvailableModelModel, ProviderModel, ModelCreatorModel, ModelTypeModel,
    UserStatusModel, UserStatusListModel,
    AssistantTypesModel, AssistantTypesListModel,
    AssistantScopesModel, AssistantScopesListModel,
    ServiceTypesModel, ServiceTypesListModel,
    ServicesModel, ServicesListModel,
    DataSourceTypesModel, DataSourceTypesListModel,
    DataSourcesModel, DataSourcesListModel,
    ChannelsModel, ChannelsListModel,
    AssistantTypesServiceTypesModel, AssistantTypesServiceTypesListModel,
    SessionTypesModel, SessionTypesListModel,
    ConnectionTypesModel, ConnectionTypesListModel,
    ConnectionProvidersModel, ConnectionProvidersListModel,
    VectorDistanceStrategiesModel, VectorDistanceStrategiesListModel,
    ConnectionProvidersVectorDistanceStrategiesModel, ConnectionProvidersVectorDistanceStrategiesListModel,
    RetrieverTypesModel, RetrieverTypesListModel,
    RetrieverStrategiesModel, RetrieverStrategiesListModel,
    VectorChannelStrategiesModel, VectorChannelStrategiesListModel,
    RunStatusesModel, RunStatusesListModel,
    AvatarsModel, AvatarsListModel,
    GuardrailTypesModel, GuardrailTypesListModel
)


class ModelsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_available_models(
            self, stage_name: str, model_type_name: Optional[str] = None, provider_name: Optional[str] = None,
            is_verified: Optional[bool] = None, model_type_id: Optional[int] = None, provider_id: Optional[int] = None,
            creator_id: Optional[int] = None, is_primary: Optional[bool] = None, name: Optional[str] = None
    ) -> List[AvailableModelModel]:
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if provider_name:
            params['provider_name'] = provider_name
        if is_verified is not None:
            params['is_verified'] = str(is_verified).lower()
        if is_primary is not None:
            params['is_primary'] = str(is_primary).lower()
        if model_type_id:
            params['model_type_id'] = model_type_id
        if provider_id:
            params['provider_id'] = provider_id
        if creator_id:
            params['creator_id'] = creator_id
        if name:
            params['name'] = name
        response = requests.get(f"{self.base_url}/available-models/", params=params)
        response.raise_for_status()
        adapter = TypeAdapter(List[AvailableModelModel])
        return adapter.validate_python(response.json())

    def get_available_model(self, available_model_id: int) -> AvailableModelModel:
        response = requests.get(f"{self.base_url}/available-models/{available_model_id}")
        response.raise_for_status()
        adapter = TypeAdapter(AvailableModelModel)
        return adapter.validate_python(response.json())

    def get_providers(self, stage_name: str, model_type_name: Optional[str] = None,
                      model_type_id: Optional[str] = None) -> List[ProviderModel]:
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if model_type_id:
            params['model_type_id'] = model_type_id
        response = requests.get(f"{self.base_url}/providers/", params=params)
        response.raise_for_status()
        adapter = TypeAdapter(List[ProviderModel])
        return adapter.validate_python(response.json())

    def get_model_creators(self, stage_name: str, model_type_name: Optional[str] = None,
                           model_type_id: Optional[str] = None) -> List[ModelCreatorModel]:
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if model_type_id:
            params['model_type_id'] = model_type_id
        response = requests.get(f"{self.base_url}/model-creators/", params=params)
        response.raise_for_status()
        adapter = TypeAdapter(List[ModelCreatorModel])
        return adapter.validate_python(response.json())


    def get_model_creator(self, creator_id: int) -> ModelCreatorModel:
        response = requests.get(f"{self.base_url}/model-creators/{creator_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ModelCreatorModel)
        return adapter.validate_python(response.json())


class FixedModelsAPI:
    """
    Provides access to fixed model data through API requests.
    This class offers the same interface as ModelsAPI but uses a different endpoint.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    # Original fixed data methods
    def get_available_models(
            self, stage_name: str, model_type_name: Optional[str] = None, provider_name: Optional[str] = None,
            is_verified: Optional[bool] = None, model_type_id: Optional[int] = None, provider_id: Optional[int] = None,
            creator_id: Optional[int] = None, is_primary: Optional[bool] = None, name: Optional[str] = None
    ) -> List[AvailableModelModel]:
        """Get a list of available fixed models with optional filtering."""
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if provider_name:
            params['provider_name'] = provider_name
        if is_verified is not None:
            params['is_verified'] = str(is_verified).lower()
        if is_primary is not None:
            params['is_primary'] = str(is_primary).lower()
        if model_type_id:
            params['model_type_id'] = model_type_id
        if provider_id:
            params['provider_id'] = provider_id
        if creator_id:
            params['creator_id'] = creator_id
        if name:
            params['name'] = name

        response = requests.get(f"{self.base_url}/available-models/", params=params)
        response.raise_for_status()
        adapter = TypeAdapter(List[AvailableModelModel])
        return adapter.validate_python(response.json())

    def get_available_model(self, available_model_id: int) -> AvailableModelModel:
        """Get details for a specific fixed model by ID."""
        response = requests.get(f"{self.base_url}/available-models/{available_model_id}")
        response.raise_for_status()
        adapter = TypeAdapter(AvailableModelModel)
        return adapter.validate_python(response.json())

    def get_providers(self, stage_name: str, model_type_name: Optional[str] = None,
                      model_type_id: Optional[str] = None) -> List[ProviderModel]:
        """Get a list of fixed providers with optional filtering."""
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if model_type_id:
            params['model_type_id'] = model_type_id

        response = requests.get(f"{self.base_url}/providers/", params=params)
        response.raise_for_status()
        adapter = TypeAdapter(List[ProviderModel])
        return adapter.validate_python(response.json())

    def get_model_creators(self, stage_name: str, model_type_name: Optional[str] = None,
                           model_type_id: Optional[str] = None) -> List[ModelCreatorModel]:
        """Get a list of fixed model creators with optional filtering."""
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if model_type_id:
            params['model_type_id'] = model_type_id

        response = requests.get(f"{self.base_url}/model-creators/", params=params)
        response.raise_for_status()
        adapter = TypeAdapter(List[ModelCreatorModel])
        return adapter.validate_python(response.json())

    def get_model_types(self) -> List[ModelTypeModel]:
        """Get a list of all fixed model types."""
        response = requests.get(f"{self.base_url}/model-types/")
        response.raise_for_status()
        adapter = TypeAdapter(List[ModelTypeModel])
        return adapter.validate_python(response.json())

    def get_model_creator(self, creator_id: int) -> ModelCreatorModel:
        """Get details for a specific fixed creator by ID."""
        response = requests.get(f"{self.base_url}/model-creators/{creator_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ModelCreatorModel)
        return adapter.validate_python(response.json())

    # New fixed data methods

    # User Status
    def get_user_statuses(self) -> List[UserStatusModel]:
        """Get a list of all user statuses."""
        response = requests.get(f"{self.base_url}/user-statuses/")
        response.raise_for_status()
        adapter = TypeAdapter(UserStatusListModel)
        return adapter.validate_python(response.json()).items

    def get_user_status(self, status_id: int) -> UserStatusModel:
        """Get details for a specific user status by ID."""
        response = requests.get(f"{self.base_url}/user-statuses/{status_id}")
        response.raise_for_status()
        adapter = TypeAdapter(UserStatusModel)
        return adapter.validate_python(response.json())

    # Assistant Types
    def get_assistant_types(self) -> List[AssistantTypesModel]:
        """Get a list of all assistant types."""
        response = requests.get(f"{self.base_url}/assistant-types/")
        response.raise_for_status()
        adapter = TypeAdapter(AssistantTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_assistant_type(self, type_id: int) -> AssistantTypesModel:
        """Get details for a specific assistant type by ID."""
        response = requests.get(f"{self.base_url}/assistant-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(AssistantTypesModel)
        return adapter.validate_python(response.json())

    # Assistant Scopes
    def get_assistant_scopes(self) -> List[AssistantScopesModel]:
        """Get a list of all assistant scopes."""
        response = requests.get(f"{self.base_url}/assistant-scopes/")
        response.raise_for_status()
        adapter = TypeAdapter(AssistantScopesListModel)
        return adapter.validate_python(response.json()).items

    def get_assistant_scope(self, scope_id: int) -> AssistantScopesModel:
        """Get details for a specific assistant scope by ID."""
        response = requests.get(f"{self.base_url}/assistant-scopes/{scope_id}")
        response.raise_for_status()
        adapter = TypeAdapter(AssistantScopesModel)
        return adapter.validate_python(response.json())

    # Service Types
    def get_service_types(self) -> List[ServiceTypesModel]:
        """Get a list of all service types."""
        response = requests.get(f"{self.base_url}/service-types/")
        response.raise_for_status()
        adapter = TypeAdapter(ServiceTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_service_type(self, type_id: int) -> ServiceTypesModel:
        """Get details for a specific service type by ID."""
        response = requests.get(f"{self.base_url}/service-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ServiceTypesModel)
        return adapter.validate_python(response.json())

    # Services
    def get_services(self) -> List[ServicesModel]:
        """Get a list of all services."""
        response = requests.get(f"{self.base_url}/services/")
        response.raise_for_status()
        adapter = TypeAdapter(ServicesListModel)
        return adapter.validate_python(response.json()).items

    def get_service(self, service_id: int) -> ServicesModel:
        """Get details for a specific service by ID."""
        response = requests.get(f"{self.base_url}/services/{service_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ServicesModel)
        return adapter.validate_python(response.json())

    # Data Source Types
    def get_data_source_types(self) -> List[DataSourceTypesModel]:
        """Get a list of all data source types."""
        response = requests.get(f"{self.base_url}/data-source-types/")
        response.raise_for_status()
        adapter = TypeAdapter(DataSourceTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_data_source_type(self, type_id: int) -> DataSourceTypesModel:
        """Get details for a specific data source type by ID."""
        response = requests.get(f"{self.base_url}/data-source-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(DataSourceTypesModel)
        return adapter.validate_python(response.json())

    # Data Sources
    def get_data_sources(self) -> List[DataSourcesModel]:
        """Get a list of all data sources."""
        response = requests.get(f"{self.base_url}/data-sources/")
        response.raise_for_status()
        adapter = TypeAdapter(DataSourcesListModel)
        return adapter.validate_python(response.json()).items

    def get_data_source(self, source_id: int) -> DataSourcesModel:
        """Get details for a specific data source by ID."""
        response = requests.get(f"{self.base_url}/data-sources/{source_id}")
        response.raise_for_status()
        adapter = TypeAdapter(DataSourcesModel)
        return adapter.validate_python(response.json())

    # Channels
    def get_channels(self) -> List[ChannelsModel]:
        """Get a list of all channels."""
        response = requests.get(f"{self.base_url}/channels/")
        response.raise_for_status()
        adapter = TypeAdapter(ChannelsListModel)
        return adapter.validate_python(response.json()).items

    def get_channel(self, channel_id: int) -> ChannelsModel:
        """Get details for a specific channel by ID."""
        response = requests.get(f"{self.base_url}/channels/{channel_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ChannelsModel)
        return adapter.validate_python(response.json())

    # Assistant Types Service Types
    def get_assistant_types_service_types(self) -> List[AssistantTypesServiceTypesModel]:
        """Get a list of all assistant types service types."""
        response = requests.get(f"{self.base_url}/assistant-types-service-types/")
        response.raise_for_status()
        adapter = TypeAdapter(AssistantTypesServiceTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_assistant_types_service_type(self, id: int) -> AssistantTypesServiceTypesModel:
        """Get details for a specific assistant types service type by ID."""
        response = requests.get(f"{self.base_url}/assistant-types-service-types/{id}")
        response.raise_for_status()
        adapter = TypeAdapter(AssistantTypesServiceTypesModel)
        return adapter.validate_python(response.json())

    # Session Types
    def get_session_types(self) -> List[SessionTypesModel]:
        """Get a list of all session types."""
        response = requests.get(f"{self.base_url}/session-types/")
        response.raise_for_status()
        adapter = TypeAdapter(SessionTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_session_type(self, type_id: int) -> SessionTypesModel:
        """Get details for a specific session type by ID."""
        response = requests.get(f"{self.base_url}/session-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(SessionTypesModel)
        return adapter.validate_python(response.json())

    # Connection Types
    def get_connection_types(self) -> List[ConnectionTypesModel]:
        """Get a list of all connection types."""
        response = requests.get(f"{self.base_url}/connection-types/")
        response.raise_for_status()
        adapter = TypeAdapter(ConnectionTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_connection_type(self, type_id: int) -> ConnectionTypesModel:
        """Get details for a specific connection type by ID."""
        response = requests.get(f"{self.base_url}/connection-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ConnectionTypesModel)
        return adapter.validate_python(response.json())

    # Connection Providers
    def get_connection_providers(self) -> List[ConnectionProvidersModel]:
        """Get a list of all connection providers."""
        response = requests.get(f"{self.base_url}/connection-providers/")
        response.raise_for_status()
        adapter = TypeAdapter(ConnectionProvidersListModel)
        return adapter.validate_python(response.json()).items

    def get_connection_provider(self, provider_id: int) -> ConnectionProvidersModel:
        """Get details for a specific connection provider by ID."""
        response = requests.get(f"{self.base_url}/connection-providers/{provider_id}")
        response.raise_for_status()
        adapter = TypeAdapter(ConnectionProvidersModel)
        return adapter.validate_python(response.json())

    # Vector Distance Strategies
    def get_vector_distance_strategies(self) -> List[VectorDistanceStrategiesModel]:
        """Get a list of all vector distance strategies."""
        response = requests.get(f"{self.base_url}/vector-distance-strategies/")
        response.raise_for_status()
        adapter = TypeAdapter(VectorDistanceStrategiesListModel)
        return adapter.validate_python(response.json()).items

    def get_vector_distance_strategy(self, strategy_id: int) -> VectorDistanceStrategiesModel:
        """Get details for a specific vector distance strategy by ID."""
        response = requests.get(f"{self.base_url}/vector-distance-strategies/{strategy_id}")
        response.raise_for_status()
        adapter = TypeAdapter(VectorDistanceStrategiesModel)
        return adapter.validate_python(response.json())

    # Connection Providers Vector Distance Strategies
    def get_connection_providers_vector_distance_strategies(self) -> List[
        ConnectionProvidersVectorDistanceStrategiesModel]:
        """Get a list of all connection providers vector distance strategies."""
        response = requests.get(f"{self.base_url}/connection-providers-vector-distance-strategies/")
        response.raise_for_status()
        adapter = TypeAdapter(ConnectionProvidersVectorDistanceStrategiesListModel)
        return adapter.validate_python(response.json()).items

    def get_connection_providers_vector_distance_strategy(self,
                                                          id: int) -> ConnectionProvidersVectorDistanceStrategiesModel:
        """Get details for a specific connection providers vector distance strategy by ID."""
        response = requests.get(f"{self.base_url}/connection-providers-vector-distance-strategies/{id}")
        response.raise_for_status()
        adapter = TypeAdapter(ConnectionProvidersVectorDistanceStrategiesModel)
        return adapter.validate_python(response.json())

    # Retriever Types
    def get_retriever_types(self) -> List[RetrieverTypesModel]:
        """Get a list of all retriever types."""
        response = requests.get(f"{self.base_url}/retriever-types/")
        response.raise_for_status()
        adapter = TypeAdapter(RetrieverTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_retriever_type(self, type_id: int) -> RetrieverTypesModel:
        """Get details for a specific retriever type by ID."""
        response = requests.get(f"{self.base_url}/retriever-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(RetrieverTypesModel)
        return adapter.validate_python(response.json())

    # Retriever Strategies
    def get_retriever_strategies(self) -> List[RetrieverStrategiesModel]:
        """Get a list of all retriever strategies."""
        response = requests.get(f"{self.base_url}/retriever-strategies/")
        response.raise_for_status()
        adapter = TypeAdapter(RetrieverStrategiesListModel)
        return adapter.validate_python(response.json()).items

    def get_retriever_strategy(self, strategy_id: int) -> RetrieverStrategiesModel:
        """Get details for a specific retriever strategy by ID."""
        response = requests.get(f"{self.base_url}/retriever-strategies/{strategy_id}")
        response.raise_for_status()
        adapter = TypeAdapter(RetrieverStrategiesModel)
        return adapter.validate_python(response.json())

    # Vector Channel Strategies
    def get_vector_channel_strategies(self) -> List[VectorChannelStrategiesModel]:
        """Get a list of all vector channel strategies."""
        response = requests.get(f"{self.base_url}/vector-channel-strategies/")
        response.raise_for_status()
        adapter = TypeAdapter(VectorChannelStrategiesListModel)
        return adapter.validate_python(response.json()).items

    def get_vector_channel_strategy(self, strategy_id: int) -> VectorChannelStrategiesModel:
        """Get details for a specific vector channel strategy by ID."""
        response = requests.get(f"{self.base_url}/vector-channel-strategies/{strategy_id}")
        response.raise_for_status()
        adapter = TypeAdapter(VectorChannelStrategiesModel)
        return adapter.validate_python(response.json())

    # Run Statuses
    def get_run_statuses(self) -> List[RunStatusesModel]:
        """Get a list of all run statuses."""
        response = requests.get(f"{self.base_url}/run-statuses/")
        response.raise_for_status()
        adapter = TypeAdapter(RunStatusesListModel)
        return adapter.validate_python(response.json()).items

    def get_run_status(self, status_id: int) -> RunStatusesModel:
        """Get details for a specific run status by ID."""
        response = requests.get(f"{self.base_url}/run-statuses/{status_id}")
        response.raise_for_status()
        adapter = TypeAdapter(RunStatusesModel)
        return adapter.validate_python(response.json())

    # Avatars
    def get_avatars(self) -> List[AvatarsModel]:
        """Get a list of all avatars."""
        response = requests.get(f"{self.base_url}/avatars/")
        response.raise_for_status()
        adapter = TypeAdapter(AvatarsListModel)
        return adapter.validate_python(response.json()).items

    def get_avatar(self, avatar_id: int) -> AvatarsModel:
        """Get details for a specific avatar by ID."""
        response = requests.get(f"{self.base_url}/avatars/{avatar_id}")
        response.raise_for_status()
        adapter = TypeAdapter(AvatarsModel)
        return adapter.validate_python(response.json())

    # Guardrail Types
    def get_guardrail_types(self) -> List[GuardrailTypesModel]:
        """Get a list of all guardrail types."""
        response = requests.get(f"{self.base_url}/guardrail-types/")
        response.raise_for_status()
        adapter = TypeAdapter(GuardrailTypesListModel)
        return adapter.validate_python(response.json()).items

    def get_guardrail_type(self, type_id: int) -> GuardrailTypesModel:
        """Get details for a specific guardrail type by ID."""
        response = requests.get(f"{self.base_url}/guardrail-types/{type_id}")
        response.raise_for_status()
        adapter = TypeAdapter(GuardrailTypesModel)
        return adapter.validate_python(response.json())

kosmoy_data = ModelsAPI('http://127.0.0.1:8000')
kosmoy_data.fixed = FixedModelsAPI('http://127.0.0.1:8000')
