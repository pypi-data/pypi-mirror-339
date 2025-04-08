# -------------------------------------------------------------------------------- #
# Astral Package - Convenience Import Wrapper
# -------------------------------------------------------------------------------- #

"""
This module provides a convenience import path for the astral-ai package.
Users can import 'from astral' instead of 'from astral_ai'.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Re-export everything from astral_ai
from astral_ai import (
    # Package metadata
    __title__,
    __version__,

    # Messages
    Message,
    MessageList,
    TextMessage,
    LocalImageMessage,
    RemoteImageMessage,

    # Completions
    Completions,
    complete,
    complete_structured,
    complete_async,
    complete_structured_async,
    
    # Errors
    AstralError,
    AuthenticationError,
    ProviderError,
    ResponseError,
    ModelNotFoundError,
)

# -------------------------------------------------------------------------------- #
# Public API
# -------------------------------------------------------------------------------- #
__all__ = [
    # Package metadata
    "__title__",
    "__version__",

    # Messages
    "Message",
    "MessageList",
    "TextMessage",
    "LocalImageMessage",
    "RemoteImageMessage",

    # Completions
    "Completions",
    "complete",
    "complete_structured",
    "complete_async",
    "complete_structured_async",
    
    # Errors
    "AstralError",
    "AuthenticationError",
    "ProviderError",
    "ResponseError",
    "ModelNotFoundError",
] 