import os
from huggingface_hub import login
from dotenv import load_dotenv

from transformers import BitsAndBytesConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline

from config import MAX_MEMORY, MODEL_ID, TRUST_REMOTE_CODE, DO_SAMPLE

import torch, platform

def check_torch_cuda():
    print("Torch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")
    print("Python:", platform.python_version())

def login_huggingface():
    load_dotenv()
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN not found in environment variables.")
    login(token=token)

def load_tokenizer(model_id: str = MODEL_ID, trust_remote_code=TRUST_REMOTE_CODE):
    return AutoTokenizer.from_pretrained(model_id, trust_remote_code=trust_remote_code)

def load_model(model_id: str = MODEL_ID, load_4bit=True, trust_remote_code=True, max_memory=MAX_MEMORY):

    print(f"🔄 Loading model: {model_id}")
    tokenizer = load_tokenizer(model_id, trust_remote_code)

    if load_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype="float16",
            bnb_4bit_use_double_quant=True,
            llm_int8_enable_fp32_cpu_offload=True
        )
    else:
        bnb_config = None

    if bnb_config:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype="auto",
            quantization_config=bnb_config,
            low_cpu_mem_usage=True,
            max_memory=max_memory,
            trust_remote_code=trust_remote_code
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype="auto",
            low_cpu_mem_usage=True,
            max_memory=max_memory,
            trust_remote_code=trust_remote_code
        )

    print(f"✅ Model loaded successfully")

    return tokenizer, model

def load_generator(model, tokenizer):
    return pipeline("text-generation", model=model, tokenizer=tokenizer, 
                     pad_token_id=tokenizer.eos_token_id, do_sample=DO_SAMPLE)