import json
import os
import re
import sys
import uuid
from typing import Dict, List, Optional

import mlx.lm
from mlxpipeline.core import (
    DEFAULT_EXTRACTION_PROMPT,
    DEFAULT_LLM_MODEL_PATH,
)


class MLXModelManager:
    """
    Singleton class to manage loaded MLX models to avoid reloading.
    """

    _instance = None
    _models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLXModelManager, cls).__new__(cls)
        return cls._instance

    def get_llm(self, model_path: str):
        """
        Get or load an MLX LLM model.

        Args:
            model_path: Path to the MLX model

        Returns:
            Tuple: (model, tokenizer)
        """
        if model_path not in self._models:
            try:
                print(f"Loading MLX LLM from {model_path}...")
                self._models[model_path] = mlx.lm.load(model_path)
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                sys.exit(1)

        return self._models[model_path]


def extract_from_chunk(
    chunk: str,
    schema: str,
    extraction_prompt: Optional[str] = None,
    llm_model_path: Optional[str] = None,
    max_tokens: int = 2048,
) -> str:
    """
    Extract structured information from a text chunk using a local MLX LLM.

    Args:
        chunk: Text chunk to extract from
        schema: JSON schema for extraction (file path or JSON string)
        extraction_prompt: Custom prompt for extraction (uses default if not specified)
        llm_model_path: Path to the MLX LLM model
        max_tokens: Maximum tokens to generate

    Returns:
        str: Extracted information in JSON format
    """
    if not llm_model_path:
        llm_model_path = DEFAULT_LLM_MODEL_PATH

    # Handle schema - could be a path or a JSON string
    if os.path.exists(schema):
        with open(schema, "r") as f:
            schema_content = f.read()
    else:
        schema_content = schema

    # Use default extraction prompt if not specified
    if not extraction_prompt:
        extraction_prompt = DEFAULT_EXTRACTION_PROMPT

    # Format the prompt
    prompt = extraction_prompt.format(text=chunk, schema=schema_content)

    # Load the model
    model_manager = MLXModelManager()
    model, tokenizer = model_manager.get_llm(llm_model_path)

    # Generate extraction
    try:
        # Tokenize the prompt
        tokens = tokenizer.encode(prompt)

        # Generate completion
        generated_tokens = mlx.lm.generate(
            model,
            tokens,
            max_tokens=max_tokens,
            temp=0.1,  # Low temperature for more deterministic output
            repetition_penalty=1.0,
        )

        # Decode the response
        response = tokenizer.decode(generated_tokens)

        # Extract JSON from response
        extracted_json = extract_json_from_response(response)

        return extracted_json
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        return json.dumps({"error": str(e)})


def extract_json_from_response(response: str) -> str:
    """
    Extract JSON from the model response.

    Args:
        response: Model response

    Returns:
        str: Extracted JSON
    """
    # Look for JSON blocks in markdown code blocks
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find anything that looks like JSON
        json_str = re.search(r"\{[\s\S]*\}", response)
        if json_str:
            json_str = json_str.group(0)
        else:
            json_str = response

    # Validate and format JSON
    try:
        parsed_json = json.loads(json_str)
        return json.dumps(parsed_json, indent=2)
    except json.JSONDecodeError:
        # If parsing fails, return the best guess at JSON
        print("Warning: Could not parse JSON from model response")
        return json_str


def extract_from_documents(
    documents: List[Dict[str, str]],
    schema: str,
    extraction_prompt: Optional[str] = None,
    llm_model_path: Optional[str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> List[str]:
    """
    Extract information from multiple documents.

    Args:
        documents: List of documents (dict with 'content' and 'source' keys)
        schema: JSON schema for extraction
        extraction_prompt: Custom prompt for extraction
        llm_model_path: Path to the MLX LLM model
        chunk_size: Maximum size of chunks
        chunk_overlap: Overlap between chunks

    Returns:
        List[str]: List of extracted information in JSON format
    """
    from mlxpipeline.chunker import chunk_text

    results = []

    for doc in documents:
        content = doc.get("content", "")
        source = doc.get("source", "unknown")

        print(f"Processing document: {source}")

        # Chunk the document
        chunks = chunk_text(content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for i, chunk in enumerate(chunks):
            print(f"  Extracting from chunk {i+1}/{len(chunks)}")

            # Extract from the chunk
            extracted = extract_from_chunk(
                chunk,
                schema=schema,
                extraction_prompt=extraction_prompt,
                llm_model_path=llm_model_path,
            )

            # Add metadata to the extracted JSON
            try:
                extracted_json = json.loads(extracted)
                extracted_json["_metadata"] = {
                    "source": source,
                    "chunk_index": i,
                    "chunk_id": str(uuid.uuid4()),
                }
                results.append(json.dumps(extracted_json, indent=2))
            except json.JSONDecodeError:
                # If parsing fails, just add the raw extraction
                results.append(extracted)

    return results
