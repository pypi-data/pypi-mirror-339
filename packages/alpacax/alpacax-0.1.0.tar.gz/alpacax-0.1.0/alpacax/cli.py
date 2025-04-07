import json
import torch
from peft import PeftModel
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import os

def run_chat():
    config_path = os.path.join(os.path.dirname(__file__), "adapters.json")
    with open(config_path, "r") as f:
        adapter_data = json.load(f)

    adapters = adapter_data["adapters"]
    default_adapter = adapter_data.get("default")

    print("\n📚 Available Adapters:")
    for name in adapters:
        print(f" - {name}")

    choice = input(f"\n🔍 Choose adapter (default: {default_adapter.split('/')[-1]}): ").strip()
    adapter_repo = adapters.get(choice, default_adapter)

    base_model = GPT2LMHeadModel.from_pretrained("SullyGreene/gpt2-alpacax-clean").to("cuda")
    tokenizer = GPT2Tokenizer.from_pretrained("SullyGreene/gpt2-alpacax-clean")
    model = PeftModel.from_pretrained(base_model, adapter_repo).to("cuda").eval()

    print("\n🧠 AlpacaX Chat | type 'exit' to quit\n")
    while True:
        user_input = input("🧑 You: ")
        if user_input.lower().strip() == "exit":
            break

        prompt = (
            "<system>\n<prompt>\nUnderstand the instruction and respond accordingly.\n</prompt>\n</system>\n"
            "<request>\n<instruction>\nRespond conversationally.\n</instruction>\n"
            f"<input>\n{user_input}\n</input>\n</request>\n<response>\n<output>\n"
        )

        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=150,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.8,
                pad_token_id=tokenizer.eos_token_id
            )

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        reply = decoded.split("</output>")[0].split("<output>")[-1].strip()
        print(f"🤖 AlpacaX: {reply}\n")
