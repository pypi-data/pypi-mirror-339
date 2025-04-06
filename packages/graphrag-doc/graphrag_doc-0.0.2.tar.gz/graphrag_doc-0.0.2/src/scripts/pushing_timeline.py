import os
import nest_asyncio
nest_asyncio.apply()
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, gpt_4o_complete, openai_embed
WORKING_DIR = "./ragdata/graphrag_index/"

async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
        addon_params={
            "insert_batch_size": 20  # Process 20 documents per batch
        }
    )

    await rag.initialize_storages()
    return rag

# Wrap the code into an async function
async def main():
    rag = await initialize_rag()

    from pathlib import Path
    import glob
    import json 
    all_timelines_p = glob.glob("/Users/xuan.tan/Projects/graphdoc/ragdata/graphrag_index/timeline3/*json")

    chunks_text = json.load(Path("/Users/xuan.tan/Projects/graphdoc/ragdata/graphrag_index_backup/kv_store_text_chunks.json").open("r"))
    docs_text = json.load(Path("/Users/xuan.tan/Projects/graphdoc/ragdata/graphrag_index_backup/kv_store_full_docs.json").open("r"))
    vdb_text_chunks = json.load(Path("/Users/xuan.tan/Projects/graphdoc/ragdata/graphrag_index_backup/vdb_chunks.json").open("r"))

    def load_json(s):
        try:
            ss = json.load(Path(s).open("r"))
            d = json.loads(ss.replace("```", "").replace("json", "")) 
            d["chunk_id"] = Path(s).stem
            return d
        except:
            return None

    all_timelines = {}
    for e in [load_json(s) for s in all_timelines_p]:
            temp = {}
            if isinstance(e, dict) and "Date" in e:
                key = e["Date"].split("T")[0]
                e["file"] = docs_text[chunks_text[e["chunk_id"]]['full_doc_id']]["content"].split("\n")[0].strip("File Name: ").strip(".txt")
                e["content"] = chunks_text[e["chunk_id"]]["content"]
                all_timelines[key] = e
    all_timeline_txt = [json.dumps(all_timelines[k]) for k in all_timelines]

    rag.insert(all_timeline_txt)

# Run the main function
import asyncio
asyncio.run(main())
