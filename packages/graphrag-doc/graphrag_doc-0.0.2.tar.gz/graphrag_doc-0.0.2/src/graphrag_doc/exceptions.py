"""Custom exceptions for GraphDoc.

This module defines custom exceptions used throughout the GraphDoc system.
"""

class GraphDocError(Exception):
    """Base exception for all GraphDoc errors."""
    pass


class ConfigurationError(GraphDocError):
    """Error raised when there's an issue with configuration."""
    pass


class ConnectionError(GraphDocError):
    """Error raised when a connection to an external service fails."""
    pass


class DocumentProcessingError(GraphDocError):
    """Error raised when document processing fails."""
    pass


class IndexingError(GraphDocError):
    """Error raised when indexing operations fail."""
    pass


class QueryError(GraphDocError):
    """Error raised when query processing fails."""
    pass


class TimelineError(GraphDocError):
    """Error raised when timeline processing fails."""
    pass


class OpenAIServiceError(GraphDocError):
    """Error raised when OpenAI API calls fail."""
    pass


class Neo4jServiceError(GraphDocError):
    """Error raised when Neo4j operations fail."""
    pass