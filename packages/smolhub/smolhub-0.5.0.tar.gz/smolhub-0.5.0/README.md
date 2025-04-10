# SmolHub

A lightweight package for fine-tuning language models using LoRA (Low-Rank Adaptation).

## Installation

```bash
pip install smolhub
```

## Usage

```python
from smolhub.scripts.finetune import SFTTrainer
from smolhub.scripts.lora import LoRAModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")

# Apply LoRA
lora_model = LoRAModel(model)

# Initialize trainer and train
trainer = SFTTrainer(
    model=lora_model,
    train_dataloader=train_dataloader,
    val_dataloader=val_dataloader,
    test_dataloader=test_dataloader,
    optimizer=optimizer,
    scheduler=scheduler
)

trainer.train()
```