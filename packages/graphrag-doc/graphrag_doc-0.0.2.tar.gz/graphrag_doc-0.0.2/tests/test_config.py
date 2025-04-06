"""Tests for configuration module.

This module tests the configuration functionality of GraphDoc.
"""

import os
from unittest.mock import patch

import pytest

from graphrag_doc.config import Config, Neo4jConfig, PathConfig, get_config


def test_neo4j_config_defaults():
    """Test Neo4j configuration defaults."""
    config = Neo4jConfig()
    assert config.uri == "bolt://localhost:7687"
    assert config.username == "neo4j"
    assert config.password == "neo4j-admin"


def test_neo4j_config_from_env():
    """Test Neo4j configuration from environment variables."""
    with patch.dict(os.environ, {
        "GRAPHDOC_NEO4J_URI": "bolt://neo4j.example.com:7687",
        "GRAPHDOC_NEO4J_USERNAME": "testuser",
        "GRAPHDOC_NEO4J_PASSWORD": "testpass"
    }):
        config = Neo4jConfig()
        assert config.uri == "bolt://neo4j.example.com:7687"
        assert config.username == "testuser"
        assert config.password == "testpass"


def test_path_config_defaults():
    """Test path configuration defaults."""
    config = PathConfig()
    assert config.index_dir == "graphrag_index"
    assert config.kv_store_text_chunks_path == "graphrag_index/kv_store_text_chunks.json"


def test_path_config_from_env():
    """Test path configuration from environment variables."""
    with patch.dict(os.environ, {
        "GRAPHDOC_INDEX_DIR": "/custom/index/path"
    }):
        config = PathConfig()
        assert config.index_dir == "/custom/index/path"
        assert config.kv_store_text_chunks_path == "/custom/index/path/kv_store_text_chunks.json"


def test_get_config():
    """Test get_config function returns a Config instance."""
    config = get_config()
    assert isinstance(config, Config)
    assert isinstance(config.neo4j, Neo4jConfig)
    assert isinstance(config.paths, PathConfig)