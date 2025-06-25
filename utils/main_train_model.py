import os
import json
import time
import pandas as pd
from config import MODELS_PATH, DATA_PATH, LOGS_PATH

from utils.prompt_utils import build_prompt
from utils.model_interactions import generate_response


def evaluate_model(model, tokenizer, model_name: str, 
                   prompts=None, max_new_tokens=100, save_dir="results",
                   do_sample=False, temperature=0.2):
    """
    Оценивает модель по фиксированным промптам, сохраняет результаты в JSON и CSV.
    """
    if prompts is None:
        prompts = [
            "Q: Кто такой Альберт Эйнштейн?\nA:",
            "Q: Объясни, как работает градиентный спуск простыми словами\nA:",
            "Q: Придумай короткий диалог между учителем и учеником на тему экологии\nA:",
            "Q: Переведи: 'I am testing a language model' и объясни перевод.\nA:",
            "Q: Придумай фантастическое животное и опиши, где оно живёт\nA:"
        ]

    results = []
    for prompt in prompts:
        print(f"🔄 {model_name}: {prompt[:60]}")
        full_prompt = build_prompt(prompt, model_name)
        start_time = time.time()
        output = generate_response(full_prompt, model, tokenizer, max_new_tokens=max_new_tokens,
                                   do_sample=do_sample, temperature=temperature)
        elapsed = round(time.time() - start_time, 2)
        results.append({
            "model": model_name,
            "prompt": prompt,
            "response": output.strip(),
            "time_sec": elapsed
        })

    # Сохраняем    
    os.makedirs(save_dir, exist_ok=True)

    json_path = os.path.join(save_dir, f"{model_name}.json")
    csv_path = os.path.join(save_dir, f"{model_name}.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    pd.DataFrame(results).to_csv(csv_path, index=False)

    print(f"✅ Результаты сохранены: {json_path}, {csv_path}")

    return results

def summarize_all_results(result_dir="results"):
    """
    Считывает все json-файлы с результатами моделей и объединяет в одну сводную таблицу.
    Возвращает DataFrame и сохраняет его в CSV.
    """
    summary = []
    
    for filename in os.listdir(result_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(result_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    summary.append(entry)

    df = pd.DataFrame(summary)
    
    # Агрегированные метрики
    summary_table = (
        df.groupby("model")
        .agg(avg_time_sec=("time_sec", "mean"), prompt_count=("prompt", "count"))
        .reset_index()
        .sort_values(by="avg_time_sec")
    )

    # Сохраняем
    summary_path = os.path.join(result_dir, "summary.csv")
    summary_table.to_csv(summary_path, index=False)

    return summary_table