"""Timeline extraction module for GraphDoc.

This module extracts timeline information from documents and stores it in a structured format.
"""

import json
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any

from neo4j import GraphDatabase
from openai import OpenAI

from graphrag_doc.config import get_config

# Get configuration
config = get_config()

# Initialize OpenAI client
client = OpenAI(api_key=config.openai.api_key)

# Connect to Neo4j
driver = GraphDatabase.driver(
    config.neo4j.uri, 
    auth=(config.neo4j.username, config.neo4j.password)
)

# Load text chunks
chunks_text = json.load(Path(config.paths.kv_store_text_chunks_path).open("r"))


def get_distinct_entity_types() -> List[str]:
    """Get all distinct entity types in the graph.
    
    Returns:
        List[str]: List of distinct entity types
    """
    query = """
    MATCH (n)
    WHERE n.entity_type IS NOT NULL
    RETURN DISTINCT n.entity_type AS entity_type
    """
    
    entity_types = []
    with driver.session() as session:
        result = session.run(query)
        entity_types = [record["entity_type"] for record in result]

    return entity_types


def get_grouped_triplets() -> Dict:
    """Get all triplets related to time entities grouped by time node.
    
    Returns:
        Dict: Dictionary of triplets grouped by time node
    """
    all_times = ['"DATE"', '"TIME"', '"TIMEFRAME"', '"TIMESTAMP"']

    query = """
    MATCH (n)-[r]-(m)
    WHERE n.entity_type IN $all_times
    RETURN n, r, m
    """
    
    grouped_triplets = defaultdict(list)  # Dictionary to group by time node

    with driver.session() as session:
        result = session.run(query, all_times=all_times)
        for record in result:
            head = record["n"]  # Extract time node properties
            relation = record["r"]  # Extract relationship type
            tail = record["m"]  # Extract related node properties

            # Convert head node properties to a hashable key
            head_key = tuple(sorted(head.items()))

            # Append relation-tail pair to the corresponding time node
            grouped_triplets[head_key].append({"relation": relation, "tail": tail})

    return grouped_triplets


def get_clean_entities(associated_entities: List[Dict]) -> List[Dict]:
    """Clean entity data by removing source_id field.
    
    Args:
        associated_entities: List of entities with their relations
        
    Returns:
        List[Dict]: Cleaned entity data
    """
    overall = []
    for entity in associated_entities:
        entity_copy = {}
        for relation_or_tail in entity:
            tmp_dict = dict(entity[relation_or_tail])
            tmp_dict.pop("source_id")
            entity_copy[relation_or_tail] = tmp_dict
        overall.append(entity_copy)
    return overall


def parse_info_from_chunk(triplet: Tuple) -> Tuple[Set[str], str]:
    """Parse information from a triplet to generate LLM prompt.
    
    Args:
        triplet: Tuple containing time entity and associated entities
        
    Returns:
        Tuple[Set[str], str]: Set of chunk IDs and generated prompt
    """
    time_entity, associated_entities = triplet
    time_chunks = time_entity[-1][1].split("<SEP>") 
    relation_chunks = list(chain.from_iterable(entity["relation"]["source_id"].split("<SEP>") for entity in associated_entities))
    tail_chunks = list(chain.from_iterable(entity["tail"]["source_id"].split("<SEP>") for entity in associated_entities))
    all_chunks = set(time_chunks + relation_chunks + tail_chunks)
    
    all_related_context = "\n".join([chunks_text[chunk_id]["content"] for chunk_id in all_chunks])
    
    prompt = f"""
The major timestamp of the event is:

**Time:** {time_entity[0][1]}

Below are all the events related to this timestamp:
{json.dumps(get_clean_entities(associated_entities))}

Relevant context is below:
{" ".join(all_related_context.split()[:8000])}

Follow below requirements to generate timeline: 
1. Action Format: Use the structure [Who] does [What] to describe each event. 
2. Summarize the events at high level as one paragraph.
3. Timestamp Standardization: Ensure all timestamps follow the MM/DD/YYYYTHH:MM:SS format.
4. Events sorted by date
5. Completing Incomplete Timestamps: If a timestamp is missing components (e.g., seconds or month), infer and complete it using context from other blocks.
6. There is one and only one time as the title, and one or multiple events associated to the time. If no event, empty response.
7. Make judgement on the quality of the timeline content. low, medium, high indicating the how much informative context it would contain.
8. Jsonify friendly

Example: 
{
    json.dumps(
        {
            "time": "02/28/2025T13:00:123",
            "event": "John submits the financial report. The system logs the submission event. An email notification is sent to Sarah for review.", 
            "importance": "high"
        }
    )
}
or the other, 
{
    json.dumps(
        {
            "time": "01/28/2025",
            "event": "event occurd", 
            "importance": "low"
        }
    )
}
or incomplete time
{
    json.dumps(
        {
            "time": "13:00:123",
            "event": "event", 
            "importance": "low"
        }
    )
}

"""
    return all_chunks, prompt


def chat_with_openai(prompt: str) -> str:
    """Generate a response using OpenAI API.
    
    Args:
        prompt: Input prompt for the model
        
    Returns:
        str: Model's response
    """
    response = client.chat.completions.create(
        model=config.openai.model,
        messages=[
            {"role": "system", "content": "You are the legal expert who can understand and summarize timeline for given case."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content


def process_timelines() -> None:
    """Process all time-related triplets and generate timeline data."""
    print("Starting timeline processing")
    grouped_data = get_grouped_triplets()
    print(f"Total triplets: {len(grouped_data)}")
    
    all_time = list(grouped_data.items())
    for idx, t in enumerate(all_time):
        print(f"Processing: {idx+1} of {len(grouped_data)}...")
        chunks_ids, prompt = parse_info_from_chunk(t)
        response = chat_with_openai(prompt)
        
        output_path = Path(config.paths.timeline_dir) / f"{idx}.json"
        with open(output_path, "w") as f:
            json.dump({"chunks_id": list(chunks_ids), "response": response}, f)
            
    print(f"Timeline processing complete. Results saved to {config.paths.timeline_dir}")


if __name__ == "__main__":
    process_timelines()