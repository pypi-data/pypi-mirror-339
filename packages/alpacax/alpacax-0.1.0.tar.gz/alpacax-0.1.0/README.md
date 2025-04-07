# 🦙 AlpacaX — LoRA-Enhanced GPT-2 CLI Chatbot

AlpacaX is a Python CLI chatbot built on top of a fine-tuned GPT-2 model with **LoRA (Low-Rank Adapters)** for modular, instruction-following interactions.  
This tool lets you **chat with different personas or skillsets** — poetry, math, philosophy — by loading lightweight LoRA adapters defined in a simple JSON config.

---

## 🚀 Features

- 🧠 Fine-tuned GPT-2 backbone (SullyGreene/gpt2-alpacax-clean)
- 🧩 Pluggable LoRA adapters for dynamic behavior
- 💬 Structured prompt format (Alpaca-style with `<instruction>`, `<input>`, `<output>`)
- ⚙️ Easy-to-edit `adapters.json` for adding new personas
- 📦 Clean CLI experience with `alpacax` command

---

## 📥 Installation

```bash
pip install alpacax
```

> Requires Python 3.8+

---

## 💡 Usage

```bash
alpacax
```

Then follow the CLI prompt to choose an adapter and start chatting.

Example conversation:

```
📚 Available Adapters:
 - poetry
 - philosophy
 - math

🔍 Choose adapter (default: poetry):
🧑 You: write a poem about the stars
🤖 AlpacaX:  
  Stars whisper through time,  
  Echoes of light in the void,  
  Dreaming in silence.
```

---

## 🔧 Configuration: `adapters.json`

This file lives inside the `alpacax` package and defines which LoRA adapters are available:

```json
{
  "default": "SullyGreene/gpt2-lora-alpacax",
  "adapters": {
    "poetry": "SullyGreene/gpt2-lora-alpacax",
    "math": "your-org/gpt2-lora-math",
    "philosophy": "your-org/gpt2-lora-philosophy"
  }
}
```

Update it to include new instruction-following LoRA adapters hosted on 🤗 Hugging Face Hub.

---

## 🛠 Development

Clone the repo and install locally for development:

```bash
git clone https://github.com/SullyGreene/AlpacaX.git
cd AlpacaX
pip install .
alpacax
```

---

## 📜 License

MIT License

---

## 🧙‍♂️ Made with magic by [Sully Greene](https://huggingface.co/SullyGreene)
