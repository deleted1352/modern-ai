from __future__ import annotations

import json
import re
from typing import List

from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extracts action items from text using a local LLM via Ollama's chat API.
    """
    if not text.strip():
        return []

    # System prompt enforcing strict structured array format
    system_prompt = (
        "You are an expert assistant that extracts action items from meeting notes.\n"
        "Analyze the provided notes and extract a clear list of actionable tasks.\n"
        "Return ONLY a valid JSON list of strings (e.g., [\"Task 1\", \"Task 2\"]).\n"
        "Do not include markdown blocks like ```json, headers, or any introductory/conversational text."
    )

    try:
        # Use the chat method matching your existing import statement
        response = chat(
            model="llama3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Notes:\n{text}"}
            ]
        )
        
        # Access content via message dictionary fields
        if hasattr(response, 'message'):
            response_text = response.message.content.strip()
        else:
            response_text = response.get("message", {}).get("content", "").strip()
        
        # Strip common markdown blocks if the LLM slips up
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            if response_text.startswith("json"):
                response_text = response_text.split("\n", 1)[-1].strip()

        # Safely parse the structural JSON array response
        extracted = json.loads(response_text)
        if isinstance(extracted, list):
            return [str(item).strip() for item in extracted if str(item).strip()]
        
        return []

    except Exception as e:
        # Fallback logging error safely to user interface
        print(f"Ollama integration error: {e}")
        return ["Error: Could not extract items via LLM. Ensure Ollama is running."]