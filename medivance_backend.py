import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Globals
tokenizer = None
model = None
generator = None
user_profile = {}
#chat_history = []

# Load model and tokenizer
def load_model(model_path):
    global tokenizer, model, generator

    print(f"🔁 Loading model from {model_path}...\n")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        device_map="auto",
        cache_dir="cache"
    ).cuda()

    generator = model.generate
    print("✅ Model loaded successfully!\n")

def gather_user_info(name, age, gender, conditions):
    user_profile["name"] = name
    user_profile["age"] = age
    user_profile["gender"] = gender
    user_profile["conditions"] = [c.strip() for c in conditions.split(",") if c.strip().lower() != "none"]


# Add this to medivance_backend.py
def generate_response(user_input, user_profile):
    exit_phrases = {"bye", "exit", "quit", "thank you", "thanks", "see you"}

    if any(phrase in user_input.lower() for phrase in exit_phrases):
        farewell = f"It was a pleasure assisting you. Take care and stay healthy, {user_profile['name']}! 👋"
        print(f"MediVance: {farewell}\n")
        return farewell

    print("📨 [generate_response] Input received:", user_input)  # 🔍 Debug input
    print("👤 [generate_response] Profile received:", user_profile)  # 🔍 Debug profile

    condition_info = (
        f"The patient has the following known conditions: {', '.join(user_profile['conditions'])}. "
        if user_profile["conditions"] else ""
    )

    # Construct personalized context
    profile_context = (
        f"You are MediVance, an intelligent and empathetic AI medical assistant developed to provide clear, accurate, and respectful responses to users' health-related concerns. "
        f"You are knowledgeable, trustworthy, and professional — always prioritize patient comfort and safety. "
        f"Speak in a warm, conversational tone while avoiding overly casual language. Provide clear and informative responses. Prioritize helpfulness and empathy over brevity. "
        f"Do not guess or mention gender-specific conditions unless explicitly indicated by the patient."
        f"The patient's name is {user_profile['name']}, they are {user_profile['age']} years old and identify as {user_profile['gender']}. "
        f"{condition_info}"
        f"If the user appears to be leaving the conversation (e.g., says 'bye', 'thanks', 'see you', etc.), end gracefully and wish them well.\n\n"
    )

    example = (
        "Here is an example conversation for your understanding:\n\n"
        "Patient: I have a sore throat, what should I do?\n"
        "MediVance: A sore throat can be caused by a variety of things like a cold, allergies, or irritation. "
        "Try drinking warm fluids, resting your voice, and using throat lozenges. Gargling salt water can also help reduce discomfort. "
        "If it lasts more than a few days or comes with a high fever, it's best to check with your doctor to rule out something more serious.\n\n"
    )

    # Append current user input to the history
    #chat_history.append(f"Patient: {user_input}")

    # Build conversation from history
    #conversation_context = "\n".join(chat_history)

    prompt = profile_context + example + f"Patient: {user_input}\nMediVance:"
    print("🧠 [generate_response] Full prompt to model:\n", prompt)  # 🔍 Debug full prompt

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    input_ids = inputs["input_ids"].cuda()
    attention_mask = inputs["attention_mask"].cuda()

    with torch.no_grad():
        generated_ids = generator(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=300,
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.05,
            num_return_sequences=1,
        )

    output_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    response = output_text[len(prompt):].split("Patient:")[0].strip()

    print("✅ [generate_response] Final model response:", response)  # 🔍 Debug final model output

    return response

