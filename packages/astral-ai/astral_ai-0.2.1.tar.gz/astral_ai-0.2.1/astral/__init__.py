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
# Import astral_ai as a module first
import astral_ai

# Then import everything from astral_ai
from astral_ai import *

# Then import specific names for better IDE support
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

# Re-export all public API symbols
__all__ = astral_ai.__all__ 