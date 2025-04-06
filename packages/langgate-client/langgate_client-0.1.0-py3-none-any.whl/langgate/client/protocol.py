"""Protocol definitions for LangGate clients."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Generic, Protocol, TypeVar

from langgate.core.logging import get_logger
from langgate.core.models import LLMInfo

logger = get_logger(__name__)


LLMInfoT = TypeVar("LLMInfoT", bound=LLMInfo, covariant=True)


class RegistryClientProtocol(Protocol[LLMInfoT]):
    """Protocol for registry clients."""

    async def get_model_info(self, model_id: str) -> LLMInfoT:
        """Get model information by ID."""
        ...

    async def list_models(self) -> Sequence[LLMInfoT]:
        """List all available models."""
        ...


class BaseRegistryClient(ABC, Generic[LLMInfoT]):
    """Base class for registry clients with common operations."""

    def __init__(self):
        """Initialize the client with cache settings."""
        self._model_cache: dict[str, LLMInfoT] = {}
        self._last_cache_refresh: datetime | None = None
        self._cache_ttl = timedelta(minutes=60)

    async def get_model_info(self, model_id: str) -> LLMInfoT:
        """Get model info with caching.

        Args:
            model_id: The ID of the model to get information for

        Returns:
            Information about the requested model

        Raises:
            ValueError: If the model is not found
        """
        if self._should_refresh_cache():
            await self._refresh_cache()

        if model_id not in self._model_cache:
            # Fetch individual model if not in cache
            model_info = await self._fetch_model_info(model_id)
            self._model_cache[model_id] = model_info
            return model_info

        return self._model_cache[model_id]

    async def list_models(self) -> Sequence[LLMInfoT]:
        """List all models with caching.

        Returns:
            A list of all available models
        """
        if self._should_refresh_cache():
            await self._refresh_cache()

        return list(self._model_cache.values())

    @abstractmethod
    async def _fetch_model_info(self, model_id: str) -> LLMInfoT:
        """Fetch model info from the source."""
        ...

    @abstractmethod
    async def _fetch_all_models(self) -> Sequence[LLMInfoT]:
        """Fetch all models from the source."""
        ...

    async def _refresh_cache(self) -> None:
        """Refresh the model cache."""
        models = await self._fetch_all_models()

        # Update cache
        self._model_cache = {model.id: model for model in models}
        self._last_cache_refresh = datetime.now()

        logger.debug("refreshed_model_cache", model_count=len(self._model_cache))

    def _should_refresh_cache(self) -> bool:
        """Check if cache should be refreshed."""
        return (
            self._last_cache_refresh is None
            or (datetime.now() - self._last_cache_refresh) > self._cache_ttl
        )
