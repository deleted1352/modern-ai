from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException

# Import your database mock/module layer 
from .. import db
# Import your newly developed LLM service processor function
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("")
def create_note(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Original heuristic creation endpoint."""
    content = str(payload.get("content", "")).strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
        
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    
    items = extract_action_items(content)
    item_ids = db.insert_action_items(items, note_id)
    action_items_response = [
        {"id": item_id, "text": item, "done": False}
        for item_id, item in zip(item_ids, items)
    ]
        
    return {
        "id": note["id"],
        "content": note["content"],
        "created_at": note["created_at"],
        "items": action_items_response
    }


# ==========================================
# TODO 4: NEW LLM EXTRACTION ENDPOINT
# ==========================================
@router.post("/extract-llm")
def create_note_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Saves a text note and utilizes Ollama local LLM to extract actionable checklist items.
    """
    content = str(payload.get("content", "")).strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
        
    # 1. Save the parent note text
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    
    # 2. Invoke our custom LLM processing chain (returns a List[str])
    items = extract_action_items_llm(content)
    
    item_ids = db.insert_action_items(items, note_id)
    action_items_response = [
        {"id": item_id, "text": item, "done": False}
        for item_id, item in zip(item_ids, items)
    ]
        
    return {
        "id": note["id"],
        "content": note["content"],
        "created_at": note["created_at"],
        "items": action_items_response
    }




# ==========================================
# TODO 4: NEW GLOBAL LIST VIEW ENDPOINT
# ==========================================
@router.get("")
def list_all_notes() -> List[Dict[str, Any]]:
    """
    Retrieves all historical saved transcripts alongside their nested check states.
    """
    try:
        all_notes = db.list_notes()
        response = []
        for note in all_notes:
            items = db.list_action_items(note_id=note["id"])
            response.append({
                "id": note["id"],
                "content": note["content"],
                "created_at": note["created_at"],
                "action_items": [
                    {"id": i["id"], "text": i["text"], "done": bool(i["done"])} for i in items
                ]
            })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database retrieval failure: {str(e)}")


@router.get("/{note_id}")
def get_single_note(note_id: int) -> Dict[str, Any]:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return {"id": row["id"], "content": row["content"], "created_at": row["created_at"]}
