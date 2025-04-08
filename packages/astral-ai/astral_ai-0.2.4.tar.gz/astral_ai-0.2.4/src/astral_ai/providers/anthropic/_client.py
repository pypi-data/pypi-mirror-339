# -------------------------------------------------------------------------------- #
# Anthropic Provider Client
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
from typing import Optional, Dict, Any, Union, TypeVar, Generic, cast

# Anthropic imports
import anthropic
from anthropic import Anthropic, AsyncAnthropic

# Astral AI Models and Types
from astral_ai.constants._models import ModelProvider, AnthropicModels
from astral_ai.providers._base_client import BaseProviderClient

# Anthropic Types
from ._types import (
    AnthropicRequestChat,
    AnthropicRequestStreaming,
    AnthropicRequestStructured,
    AnthropicStructuredResponseType,
    AnthropicChatResponseType,
    AnthropicStreamingResponseType,
    AnthropicSyncClientType,
    AnthropicAsyncClientType,
)

# Exceptions
from astral_ai.errors.exceptions import (
    AstralProviderResponseError,
    AstralAuthMethodFailureError,
    AstralMissingCredentialsError
)
from astral_ai.errors.error_decorators import provider_error_handler

# Astral Auth
from astral_ai._auth import AUTH_CONFIG_TYPE, auth_method, AUTH_ENV_VARS, AUTH_METHOD_NAMES

from astral_ai.logger import logger

# -------------------------------------------------------------------------------- #
# Anthropic Provider Client
# -------------------------------------------------------------------------------- #

class AnthropicProviderClient(BaseProviderClient[
        AnthropicSyncClientType,
        AnthropicAsyncClientType,
        AnthropicRequestChat,
        AnthropicRequestStructured,
        AnthropicRequestStreaming,
        AnthropicChatResponseType,
        AnthropicStructuredResponseType,
        AnthropicStreamingResponseType]):
    """
    Client for Anthropic.
    """

    # --------------------------------------------------------------------------
    # Model Provider
    # --------------------------------------------------------------------------

    _model_provider: ModelProvider = "anthropic"

    # --------------------------------------------------------------------------
    # Client Properties with Explicit Type Annotations
    # --------------------------------------------------------------------------
    
    # @property
    # def client(self) -> AnthropicSyncClientType:
    #     """
    #     Returns the synchronous Anthropic client.
        
    #     Returns:
    #         AnthropicSyncClientType: The synchronous Anthropic client
    #     """
    #     return cast(AnthropicSyncClientType, super().client)
    
    # @property
    # def async_client(self) -> AnthropicAsyncClientType:
    #     """
    #     Returns the asynchronous Anthropic client.
        
    #     Returns:
    #         AnthropicAsyncClientType: The asynchronous Anthropic client
    #     """
    #     return cast(AnthropicAsyncClientType, super().async_client)

    # --------------------------------------------------------------------------
    # Initialize
    # --------------------------------------------------------------------------
    def __init__(self, config: Optional[AUTH_CONFIG_TYPE] = None, async_client: bool = False):
        # Initialize the base class (which performs authentication)
        super().__init__(config, async_client)

    # --------------------------------------------------------------------------
    # Validate Credentials
    # --------------------------------------------------------------------------

    def _validate_credentials(self, auth_method_name: AUTH_METHOD_NAMES, config: AUTH_CONFIG_TYPE, env: AUTH_ENV_VARS) -> Dict[str, str]:
        """
        Validate the credentials for the Anthropic provider.
        """
        credentials = {}

        if auth_method_name == "api_key":
            credentials["api_key"] = config.get(self._model_provider, {}).get(auth_method_name, None) or env.get("ANTHROPIC_API_KEY")
            if not credentials["api_key"]:
                raise AstralAuthMethodFailureError("API key is required")

            return credentials
        else:
            raise AstralMissingCredentialsError(
                f"Invalid authentication method: {auth_method_name}",
                auth_method_name=auth_method_name,
                provider_name=self._model_provider,
                required_credentials=["api_key"],
                missing_credentials=[auth_method_name]
            )

    # --------------------------------------------------------------------------
    # Authenticate
    # --------------------------------------------------------------------------

    @auth_method("api_key")
    def auth_via_api_key(self, config: AUTH_CONFIG_TYPE, env: AUTH_ENV_VARS, async_client: bool = False) -> Union[AnthropicSyncClientType, AnthropicAsyncClientType]:
        """
        Authenticate using an API key from config or environment variables.

        Args:
            config: Configuration dictionary
            env: Environment variables dictionary
            async_client: Whether to initialize an async client
        """

        credentials = self._validate_credentials(
            auth_method_name="api_key",
            config=config,
            env=env
        )

        # Extract the credentials
        api_key = credentials["api_key"]

        if async_client:
            return AsyncAnthropic(api_key=api_key)
        else:
            return Anthropic(api_key=api_key)

    # --------------------------------------------------------------------------
    # Create Completion
    # --------------------------------------------------------------------------

    @provider_error_handler
    def create_completion_chat(self, request: AnthropicRequestChat) -> AnthropicChatResponseType:
        """
        Create a completion using the Anthropic API.

        Args:
            request: The request to create a completion.

        Returns:
            The completion.
        """
        anthropic_response = self.client.messages.create(**request)

        if isinstance(anthropic_response, AnthropicChatResponseType):
            return anthropic_response
        else:
            raise AstralProviderResponseError(
                f"Unexpected response type from {self._model_provider}",
                provider_name=self._model_provider,
                expected_response_type="AnthropicChatResponse"
            )

    # --------------------------------------------------------------------------
    # Create Completion Async
    # --------------------------------------------------------------------------

    @provider_error_handler
    async def create_completion_chat_async(self, request: AnthropicRequestChat) -> AnthropicChatResponseType:
        """
        Create a completion asynchronously using the Anthropic API.

        Args:
            request: The request to create a completion.

        Returns:
            The completion.
        """
        anthropic_response = await self.async_client.messages.create(**request)

        if isinstance(anthropic_response, AnthropicChatResponseType):
            return anthropic_response
        else:
            raise AstralProviderResponseError(
                f"Unexpected response type from {self._model_provider}",
                provider_name=self._model_provider,
                expected_response_type="AnthropicChatResponse"
            )

    # --------------------------------------------------------------------------
    # Create Structured Completion
    # --------------------------------------------------------------------------

    @provider_error_handler
    def create_completion_structured(self, request: AnthropicRequestStructured) -> AnthropicStructuredResponseType:
        """
        Create a structured completion using the Anthropic API.

        Note: Anthropic doesn't natively support structured outputs in the same way as OpenAI.
        This implementation will need custom parsing of the response.

        Args:
            request: The request to create a structured completion.

        Returns:
            The structured completion.
        """
        # Note: Anthropic doesn't have a native parse method like OpenAI
        # We're using the standard message creation and will handle parsing elsewhere
        anthropic_response = self.client.messages.create(**request)

        if isinstance(anthropic_response, AnthropicStructuredResponseType):
            return anthropic_response
        else:
            raise AstralProviderResponseError(
                f"Unexpected response type from {self._model_provider}",
                provider_name=self._model_provider,
                expected_response_type="AnthropicStructuredResponse"
            )

    # --------------------------------------------------------------------------
    # Create Structured Completion Async
    # --------------------------------------------------------------------------

    @provider_error_handler
    async def create_completion_structured_async(self, request: AnthropicRequestStructured) -> AnthropicStructuredResponseType:
        """
        Create a structured completion asynchronously using the Anthropic API.

        Note: Anthropic doesn't natively support structured outputs in the same way as OpenAI.
        This implementation will need custom parsing of the response.

        Args:
            request: The request to create a structured completion.

        Returns:
            The structured completion.
        """
        # Note: Anthropic doesn't have a native parse method like OpenAI
        # We're using the standard message creation and will handle parsing elsewhere
        anthropic_response = await self.async_client.messages.create(**request)

        if isinstance(anthropic_response, AnthropicStructuredResponseType):
            return anthropic_response
        else:
            raise AstralProviderResponseError(
                f"Unexpected response type from {self._model_provider}",
                provider_name=self._model_provider,
                expected_response_type="AnthropicStructuredResponse"
            )
