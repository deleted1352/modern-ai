import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
<<<<<<< HEAD
YOUR_SYSTEM_PROMPT = (
    "You are an exact string reversal function. Output ONLY the final reversed word. No chatter.\n\n"
    "Example 1:\n"
    "Input: cat\n"
    "Step-by-step: c -> a -> t\n"
    "Reversed step-by-step: t -> a -> c\n"
    "Output: tac\n\n"
    "Example 2:\n"
    "Input: strawberry\n"
    "Step-by-step: s -> t -> r -> a -> w -> b -> e -> r -> r -> y\n"
    "Reversed step-by-step: y -> r -> r -> e -> b -> w -> a -> r -> t -> s\n"
    "Output: yrrebwarts\n\n"
    "Example 3:\n"
    "Input: pineapple\n"
    "Step-by-step: p -> i -> n -> e -> a -> p -> p -> l -> e\n"
    "Reversed step-by-step: e -> l -> p -> p -> a -> e -> n -> i -> p\n"
    "Output: elppaenip\n\n"
    "Example 4:\n"
    "Input: httpstatus\n"
    "Step-by-step: h -> t -> t -> p -> s -> t -> a -> t -> u -> s\n"
    "Reversed step-by-step: s -> u -> t -> a -> t -> s -> p -> t -> t -> h\n"
    "Output: sutatsptth"
)
=======
YOUR_SYSTEM_PROMPT = ""
>>>>>>> 3676885c8c867ceb12b35d1b370bf0045a674297

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
