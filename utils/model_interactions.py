from config import MAX_TOKENS, BASE_DIR
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# load key
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found")
openai_key = openai_key.strip()

# new client
clientOpenAI = OpenAI(api_key=openai_key, project="proj_JaNxEwOgdIt5HgqdzL4eULHS")

def generate_response(generator, prompt, max_tokens=MAX_TOKENS):
    """
    Generate text from the model
    """
    out = generator(prompt, max_new_tokens=max_tokens)[0]["generated_text"]
    return out

def generate_response_openai(system: str, instruction: str, model="gpt-4", max_tokens=768) -> str:
    response = clientOpenAI.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": instruction}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    content = response.choices[0].message.content
    if content is None:
        return ""
    return content.strip()

def build_prompt(system, instruction):
    return f"<|system|>\n{system}\n<|user|>\n{instruction}\n<|assistant|>\n"