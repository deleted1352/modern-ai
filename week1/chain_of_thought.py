import os
import re
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = (
    "You are a precise mathematical reasoning agent. You must think step-by-step to "
    "solve modular exponentiation problems. Always find the repeating pattern (cycle) "
    "of the base modulo 100 first, reduce the large exponent by that cycle length, and "
    "then compute the final remainder.\n\n"
    "Here is an example of the step-by-step reasoning pattern you must follow:\n"
    "--- EXAMPLE TASK ---\n"
    "Problem: What is 7^{42} (mod 100)?\n"
    "Step 1: Analyze the cycle of powers of 7 modulo 100:\n"
    "  - 7^1 = 7\n"
    "  - 7^2 = 49\n"
    "  - 7^3 = 343 => 43 (mod 100)\n"
    "  - 7^4 = 7 * 43 = 301 => 1 (mod 100)\n"
    "The remainder reaches 1 at 7^4, meaning the powers repeat in a cycle of length 4.\n"
    "Step 2: Reduce the exponent 42 by dividing it by the cycle length (4):\n"
    "  - 42 / 4 = 10 with a remainder of 2. Therefore, 42 => 2 (mod 4).\n"
    "Step 3: Evaluate the base raised to the remainder power:\n"
    "  - 7^42 => 7^2 (mod 100)\n"
    "  - 7^2 = 49\n"
    "Answer: 49\n"
    "--- END OF EXAMPLE ---\n\n"
    "Apply this exact cycle-finding logic to the user's problem. Break down the powers, "
    "find the cycle length, reduce the exponent, and state the final result.\n"
    "On the very last line of your response, you MUST output the answer exactly in this "
    "format: 'Answer: <number>'."
)


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace.

    - Finds the LAST line that starts with 'Answer:' (case-insensitive)
    - Normalizes to 'Answer: <number>' when a number is present
    - Falls back to returning the matched content if no number is detected
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)


