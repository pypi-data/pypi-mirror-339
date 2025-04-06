import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, gpt_4o_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger

setup_logger("lightrag", level="DEBUG")

async def initialize_rag():
    rag = LightRAG(
        working_dir="./test_rag",
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag

def main():
    # Initialize RAG instance
    with open("/Users/xuan.tan/Projects/graphdoc/README.md", "r") as f:
        txt = f.read()
    rag = asyncio.run(initialize_rag())
    # Insert text
    rag.insert([txt])
    mode="mix"

    rag.query(
        "summarize this project?",
        param=QueryParam(mode=mode)
    )

if __name__ == "__main__":
    main()