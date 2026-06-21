from unittest.mock import MagicMock, patch

from ..app.services.extract import extract_action_items, extract_action_items_llm

BULLET_NOTES = """
Notes from meeting:
- [ ] Set up database
* implement API extract endpoint
1. Write tests
Some narrative sentence.
""".strip()


def test_extract_bullets_and_checkboxes():
    items = extract_action_items(BULLET_NOTES)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_parses_bullet_list(mock_chat):
    """Mocked LLM returns a JSON array parsed from bullet-style meeting notes."""
    mock_chat.return_value = {
        "message": {
            "content": (
                '["Set up database", "implement API extract endpoint", "Write tests"]'
            )
        }
    }

    items = extract_action_items_llm(BULLET_NOTES)

    assert items == [
        "Set up database",
        "implement API extract endpoint",
        "Write tests",
    ]
    mock_chat.assert_called_once_with(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that extracts action items from meeting notes.\n"
                    "Analyze the provided notes and extract a clear list of actionable tasks.\n"
                    'Return ONLY a valid JSON list of strings (e.g., ["Task 1", "Task 2"]).\n'
                    "Do not include markdown blocks like ```json, headers, or any introductory/conversational text."
                ),
            },
            {"role": "user", "content": f"Notes:\n{BULLET_NOTES}"},
        ],
    )


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_parses_bullet_list_object_response(mock_chat):
    """Ollama SDK responses expose content via response.message.content."""
    mock_response = MagicMock()
    mock_response.message.content = (
        '["Set up database", "implement API extract endpoint", "Write tests"]'
    )
    mock_chat.return_value = mock_response

    items = extract_action_items_llm(BULLET_NOTES)

    assert items == [
        "Set up database",
        "implement API extract endpoint",
        "Write tests",
    ]


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_empty_input(mock_chat):
    """Empty or whitespace-only input returns [] without calling Ollama."""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("     ") == []
    assert extract_action_items_llm("\n\t  \n") == []
    mock_chat.assert_not_called()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_connection_error(mock_chat):
    """Ollama failures surface a single user-facing error item."""
    mock_chat.side_effect = ConnectionError("Ollama server unavailable")

    items = extract_action_items_llm(BULLET_NOTES)

    assert items == [
        "Error: Could not extract items via LLM. Ensure Ollama is running."
    ]
    mock_chat.assert_called_once()
