# data_preparation_utils.py

from docx import Document
import json
from tqdm import tqdm
from transformers import pipeline
from config import SYSTEM_PROMPT

from utils.utils import load_model
from utils.prompt_utils import build_prompt
from utils.model_interactions import generate_response

import openai

def extract_blocks_from_docx(path):
    """
    Read a document and split it into meaningful blocks
    """
    doc = Document(path)
    blocks, current = [], []
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            current.append(text)
        elif current:
            blocks.append("\n".join(current))
            current = []
    if current:
        blocks.append("\n".join(current))
    return blocks

def block_to_sample(dialog_text: str) -> dict:
    """
    Convert a dialog text to a sample
    """
    level = "A2"
    if "Rollenspiel" in dialog_text:
        task_type = "roleplay"
    elif "Fragen" in dialog_text:
        task_type = "questions"
    else:
        task_type = "dialog"

    instruction = (
        f"Разбери следующий {task_type} между продавцом и покупателем. "
        f"Уровень {level}. Ответь, были ли ошибки, и предложи похожее упражнение.\n\n"
        + dialog_text.strip()
    )

    return {
        "system": SYSTEM_PROMPT,
        "instruction": instruction,
        "response": "",
        "metadata": {"level": level, "type": task_type}
    }

def is_valid_block(text):
    """
    Filter out short or irrelevant blocks
    """
    return len(text.split()) > 5 and ("Kunde" in text or "Verkäufer" in text or "Du" in text)

def prepare_dataset_from_docx(docx_path, output_path, model_id):
    """
    Full cycle: from docx to ready .jsonl with answers
    """
    print("📄 Reading and filtering blocks...")
    raw_blocks = extract_blocks_from_docx(docx_path)
    valid_blocks = [b for b in raw_blocks if is_valid_block(b)]
    print(f"🔹 Total blocks: {len(raw_blocks)}, after filtering: {len(valid_blocks)}")

    samples = [block_to_sample(b) for b in valid_blocks]

    tokenizer, model = load_model(model_id=model_id)

    generator = pipeline("text-generation", model=model, tokenizer=tokenizer,
                         pad_token_id=tokenizer.eos_token_id, do_sample=False)

    print("✏️ Generating answers...")
    for s in tqdm(samples, desc="Generating"):
        prompt = build_prompt(s["system"], s["instruction"])
        s["response"] = generate_response(generator, prompt)

    print(f"💾 Saving to {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        for s in samples:
            json.dump(s, f, ensure_ascii=False)
            f.write("\n")
    print("✅ Done!")

def tokenize(example, tokenizer):
    messages = example["messages"]
    full_text = ""
    for msg in messages:
        full_text += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
    full_text += "<|im_start|>assistant\n"  
    return tokenizer(full_text, truncation=True, max_length=1024)

def format_to_messages(example):
    return {
        "messages": [
            {"role": "system", "content": example["system"]},
            {"role": "user", "content": example["instruction"]},
            {"role": "assistant", "content": example["response"]}
        ]
    }