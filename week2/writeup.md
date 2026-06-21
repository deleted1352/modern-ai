# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Ethan Chen \

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```text
Analyze the existing extract_action_items() function in week2/app/services/extract.py, which currently extracts action items using predefined heuristics. Your task is to implement an LLM-powered alternative, extract_action_items_llm(), that utilizes Ollama to perform action item extraction via a large language model.
``` 

Generated Code Snippets:
```python
# week2/app/services/extract.py (Lines 63+)
def extract_action_items_llm(text: str) -> List[str]:
    """
    Extracts action items from text using a local LLM via Ollama's chat API.
    """
    if not text.strip():
        return []

    system_prompt = (
        "You are an expert assistant. Extract a clear, numbered or bulleted list "
        "of actionable tasks or TODOs from the provided text. Do not include "
        "introductory or concluding conversational text. Only return the tasks."
    )
    # uses chat method and strips out leading numbered digits/markdown blocks gracefully
```

### Exercise 2: Add Unit Tests
Prompt: 
```text
Write unit tests for extract_action_items_llm() covering multiple inputs (e.g., bullet lists, keyword-prefixed lines, empty input) in week2/tests/test_extract.py. Use mocking so tests run fast and don't require an active Ollama backend server.
``` 

Generated Code Snippets:
```python
# week2/tests/test_extract.py (Lines 19+)
@patch('week2.app.services.extract.chat')
def test_extract_action_items_llm_success(mock_chat):
    # Simulated successful LLM payload responses
    
def test_extract_action_items_llm_empty_input():
    # Enforces fast-path short circuit returns
    
@patch('week2.app.services.extract.chat')
def test_extract_action_items_llm_connection_error(mock_chat):
    # Safe isolation intercepting operational system crashes
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```text
Perform a refactor of the code in the backend, focusing in particular on well-defined API contracts/schemas, database layer cleanup, app lifecycle/configuration, error handling. Fix parameter signature order mismatches for db storage lookups.
``` 

Generated/Modified Code Snippets:
```python
# week2/app/routers/notes.py (Lines 45-75)
# Swapped routing insertion parameters from db.insert_action_items(note_id, items)
# to match db.py function signature expectations exactly:
db.insert_action_items(items, note_id)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```text
Integrate the LLM-powered extraction as a new endpoint. Update the frontend to include an "Extract LLM" button that, when clicked, triggers the extraction process via the new endpoint. Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" button that, when clicked, fetches and displays them.
``` 

Generated Code Snippets:
```python
# week2/app/routers/notes.py (Lines 40+)
@router.post("/extract-llm")
def create_note_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Persists parent note transcript, pulls LLM tasks, synchronizes checklist data bulk payloads

@router.get("")
def list_all_notes() -> List[Dict[str, Any]]:
    # Pulls all historic cards out of structural tables
```
```html
<!-- week2/frontend/index.html (Lines 32+, 50+) -->
<button id="extract_llm">Extract (LLM AI)</button>
<button id="list_notes">📋 List All Notes</button>
<div id="notes_list"></div>
<!-- Configured event listener handlers dispatching fetches via matching endpoints -->
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```text
Use Cursor to analyze the current codebase and generate a well-structured README.md file covering a project overview, environment/conda setups, api endpoints, and test suite commands.
``` 

Generated Code Snippets:
```markdown
# README.md (Entire File created in Project Root)
- Project summary framework details.
- Initialization instructions via poetry.
- REST routing roadmap index definitions.
- Local execution matrix commands matching pytest engines.
```


## SUBMISSION INSTRUCTIONS
Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 