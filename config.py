# config.py

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
MODELS_PATH = BASE_DIR / "models"
DATA_PATH = BASE_DIR / "data"
LOGS_PATH = BASE_DIR / "logs"
RESULTS_PATH = BASE_DIR / "results"
CHECKPOINT_PATH = MODELS_PATH / "checkpoint-3"

# Model
MODEL_ID = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
TRUST_REMOTE_CODE = True

# Finetune
USE_4BIT = True
LORA_CONFIG = {
    "r": 8,
    "lora_alpha": 32,
    "target_modules": ["q_proj", "v_proj"],
    "lora_dropout": 0.1,
    "bias": "none",
    "task_type": "CAUSAL_LM"
}
BNB_4BIT_CONFIG = {
    "load_in_4bit": True,
    "bnb_4bit_use_double_quant": True,
    "bnb_4bit_compute_dtype": "bfloat16",
    "bnb_4bit_quant_type": "nf4"         
}
TRAINING_ARGS = {
    "output_dir": "../models",
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "num_train_epochs": 3,
    "logging_dir": "../logs",
    "logging_steps": 5,
    "save_steps": 50,
    "save_total_limit": 2,
    "report_to": "tensorboard",
    "disable_tqdm": False,
    "logging_first_step": True,
    "lr_scheduler_type": "cosine",
    "warmup_steps": 10,
    "learning_rate": 2e-4,
    "fp16": True
}

# System prompt
SYSTEM_PROMPT = (
    "Ты — преподаватель немецкого языка для русскоязычных студентов уровня A2. "
    "Сначала проанализируй диалог: укажи, есть ли ошибки, объясни их. "
    "Объяснение давай на русском языке. "
    "Затем предложи похожее упражнение на основе темы диалога. "
    "Отвечай строго по делу, без лишних вступлений."
)
TEMPLATE_TYPES = ["dialog_error_fix", "dialog_extend", "grammar_explanation", "fill_in_the_blank", "dialog_analysis"]

# Generation
USE_OPENAI_GENERATION = True
MAX_TOKENS = 512
TEMPERATURE = 0.2
DO_SAMPLE = False
MAX_MEMORY = {0: "12GiB", "cpu": "16GiB"}
