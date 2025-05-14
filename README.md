
# Medivance: Personalized Healthcare Advisor 

**Medivance** is a lightweight, domain-specific medical chatbot powered by a fine-tuned [TinyLLaMA-1.1B Chat](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) model using **LoRA** (Low-Rank Adaptation). Developed as a capstone project, it demonstrates the practical integration of cutting-edge NLP with full-stack deployment to deliver responsive and resource-efficient medical assistance.



## Project Overview

Medivance simulates intelligent, medically informed conversations—particularly useful in low-resource environments. The model is fine-tuned on curated medical datasets to provide accurate, safe, and context-aware responses.

### Highlights:
- Fine-tuned on real-world, domain-specific medical data  
- Optimized for 4GB VRAM GPUs  
- Full-stack deployment (Flask backend + HTML/CSS/JS frontend)  
- Lightweight, animated, and asynchronous chat interface  



## Tech Stack

| Component     | Technology                        |
|---------------|------------------------------------|
| Model         | TinyLLaMA-1.1B                     |
| Fine-tuning   | LoRA via HuggingFace PEFT         |
| Backend       | Python, Flask                      |
| Frontend      | HTML, CSS, JavaScript      |
| Training Env  | Kaggle (Tesla P100 GPU)            |
| Deployment    | Localhost (Windows 10/11)          |


## Project Structure

```bash
medivance/
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   └── profile.html
│   ├── static/
│   │   ├── style.css
│   │   ├── profilestyle.css
│   │   ├── script.js
│   │   └── images/
│   │       └── [frontend image assets]
├── backend/
│   ├── medivance_backend.py
│   └── frontend.py
├── training/
│   ├── tinyllama_lora_training_part1.ipynb
│   └── tinyllama_lora_training_part2.ipynb
├── dataset/
│   └── merged_final_dataset.json
├── adapter_model.bin
└── README.md
```



## Model Training Pipeline

- **Sources**: iCliniq, HealthCareMagic, GenMedGPT, and custom CSV
- **Preprocessing**: All data was standardized into **Alpaca format** (`instruction`, `input`, `output`)
- **Fine-tuning**:
  - Base: TinyLLaMA-1.1B
  - Method: LoRA using HuggingFace PEFT
  - Platform: Kaggle (Tesla P100 GPU)
  - Output: `adapter_model.bin` (LoRA weights)



## How to Run Locally (Windows)

### Prerequisites

- Python 3.10+
- Install dependencies: `transformers`, `peft`, `torch`, `flask`, `accelerate`, `safetensors`

### Setup

```bash
git clone https://github.com/Hari8124/medivance.git
cd medivance
```

### Start the Backend

```bash
cd backend
python frontend.py
```

### Launch the Frontend

Open `frontend/index.html` in your browser, or use Live Server in VS Code.

### Screenshots

Here are some screenshots of the Medivance chatbot in action:

![Image 1](https://drive.google.com/uc?export=view&id=1uIKzNXgmRjWdlqHR0JmRWqhLlrN8KPNe)
![Image 2](https://drive.google.com/uc?export=view&id=1Y7_LCO66VBKTLBiA28yx-spDFrFpNJdq)
![Image 3](https://drive.google.com/uc?export=view&id=1KlSCsFEGJ3LRzmIqeQl82F9lOpJOI6in)
![Image 4](https://drive.google.com/uc?export=view&id=1AVoqVSFaslzNDCEXEmg5dDxgSGnEscVW)

## Example Inference

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

tokenizer = AutoTokenizer.from_pretrained("TinyLLaMA-1.1B")
base_model = AutoModelForCausalLM.from_pretrained("TinyLLaMA-1.1B")
model = PeftModel.from_pretrained(base_model, "adapter_model.bin")

query = "What are the symptoms of diabetes?"
inputs = tokenizer(query, return_tensors="pt").input_ids
outputs = model.generate(inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```



## Future Enhancements

- ✅ Multi-turn memory and context retention  
- ✅ Voice input support  
- ✅ Mobile app or PWA version  
- ✅ Integration with real-time health APIs  
- ✅ Patient profile authentication  



## Disclaimer

This chatbot is intended **solely for educational and demonstration purposes**. It is **not a substitute for licensed medical professionals**. Always consult a certified healthcare provider for actual medical advice.


## Acknowledgements

- **Project Guide**: Dr. Kumaresan P, VIT Vellore  
- **Dataset Sources**: iCliniq, HealthCareMagic, GenMedGPT  
- **Fine-tuning Platform**: Kaggle (Tesla P100 GPU)  
