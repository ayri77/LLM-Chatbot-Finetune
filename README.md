# LLM-Chatbot-Finetune

This project focuses on fine-tuning a pre-trained language model (LLM) to create a more personalized and domain-adapted chatbot. The goal is to explore fine-tuning techniques (LoRA, QLoRA) using real-world conversational data from previous chatbot applications and educational materials.

## Goals
- Learn and implement LLM fine-tuning workflows
- Understand the transformer architecture through hands-on experiments
- Build a customizable chatbot capable of adapting to new domains
- Test various models (Mistral, Phi-2, etc.) and techniques (instruction tuning, conversational fine-tuning)

## Tools & Stack
- PyTorch, Hugging Face Transformers
- LoRA / QLoRA for efficient fine-tuning
- Weights & Biases (optional) for experiment tracking
- Streamlit or Gradio for frontend UI

## Current Status
✅ Project structure initialized  
⏳ Preparing dataset and scripts for fine-tuning  
🔜 Model evaluation and chatbot deployment  

---

## Requirements

- Python 3.9+
- See `requirements.txt` for all dependencies

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Quickstart

1. **Clone the repository:**
   ```bash
git clone <repo-url>
cd LLM_Chatbot-Finetune
```

2. **Set up your environment:**
   - (Optional) Create a virtual environment:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Prepare your data:**
   - Place your training and evaluation data in the `data/` directory.
   - See the `notebooks/` for data preparation and exploration workflows.

4. **Run the API server:**
   ```bash
   python chatbot/start_server.py
   ```
   - The API will be available at `http://localhost:8000` by default.

5. **Jupyter Notebooks:**
   - Explore and run the notebooks in the `notebooks/` directory for data analysis, model training, and evaluation.
   - Start Jupyter:
     ```bash
     jupyter notebook
     ```

---

## Project Structure

- `chatbot/` - Main application code (API, models, utilities)
- `data/` - Training and evaluation datasets
- `models/` - Saved and fine-tuned model checkpoints
- `notebooks/` - Jupyter notebooks for exploration and experiments
- `results/` - Model outputs and evaluation results
- `scripts/` - Utility scripts for training and preprocessing
- `logs/` - Training and inference logs

---

## .gitignore

The `.gitignore` is configured to exclude:
- Python cache files, virtual environments
- Data, models, logs, and results
- Jupyter checkpoints and notebook outputs
- OS and IDE-specific files

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

---

## License

This project is licensed under the MIT License.
