"""Configuration management for GraphDoc.

This module provides centralized configuration management for the GraphDoc system,
loading settings from environment variables and config files.
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel


class Neo4jConfig(BaseModel):
    """Neo4j database connection configuration."""
    
    uri: str = os.environ.get("GRAPHDOC_NEO4J_URI", "bolt://localhost:7687")
    username: str = os.environ.get("GRAPHDOC_NEO4J_USERNAME", "neo4j")
    password: str = os.environ.get("GRAPHDOC_NEO4J_PASSWORD", "neo4j-admin")


class PathConfig(BaseModel):
    """Path configuration for data files and storage."""
    
    index_dir: str = os.environ.get("GRAPHDOC_INDEX_DIR", "graphrag_index")
    
    @property
    def kv_store_text_chunks_path(self) -> str:
        """Path to the text chunks KV store."""
        return os.path.join(self.index_dir, "kv_store_text_chunks.json")
    
    @property
    def kv_store_doc_status_path(self) -> str:
        """Path to the document status KV store."""
        return os.path.join(self.index_dir, "kv_store_doc_status.json")
    
    @property
    def kv_store_full_docs_path(self) -> str:
        """Path to the full documents KV store."""
        return os.path.join(self.index_dir, "kv_store_full_docs.json")
    
    @property
    def kv_store_llm_response_cache_path(self) -> str:
        """Path to the LLM response cache KV store."""
        return os.path.join(self.index_dir, "kv_store_llm_response_cache.json")
    
    @property
    def timeline_dir(self) -> str:
        """Path to the timeline directory."""
        timeline_path = os.path.join(self.index_dir, "timeline")
        os.makedirs(timeline_path, exist_ok=True)
        return timeline_path


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""
    
    api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
    model: str = os.environ.get("GRAPHDOC_OPENAI_MODEL", "gpt-4o-mini")


class Config(BaseModel):
    """Main configuration class for GraphDoc."""
    
    neo4j: Neo4jConfig = Neo4jConfig()
    paths: PathConfig = PathConfig()
    openai: OpenAIConfig = OpenAIConfig()


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance.
    
    Returns:
        Config: The global configuration object
    """
    return config