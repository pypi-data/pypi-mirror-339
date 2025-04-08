
from greaterprompt import GreaterDataloader

dataset2 = GreaterDataloader(custom_inputs=[
    {
        "question": "((-1 + 2 + 9 * 5) - (-2 + -4 + -4 * -7)) =", 
        "prompt": "Use logical reasoning and think step by step.", 
        "answer": "24"
    },
    {
        "question": "((-9 * -5 - 6 + -2) - (-8 - -6 * -3 * 1)) =",
        "prompt": "Use logical reasoning and think step by step.",
        "answer": "63"
     },
    {
        "question": "((3 * -3 * 6 + -5) - (-2 + -7 - 7 - -7)) =",
        "prompt": "Use logical reasoning and think step by step.",
        "answer": "-50"
    }
])

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/scratch1/wmz5132/models/huggingface/gemma-2-9b-it"
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, torch_dtype=torch.bfloat16, device_map='cuda:1'
)
model.gradient_checkpointing_enable() #to save the cuda memory
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)


from torch.nn import functional as F

# for GreaterOptimizer
greater_optimize_config = {
    "intersect_q": 5,
    "candidates_topk": 10,
    "loss_function": F.cross_entropy,
    "perplexity_loss": True,
    "perplexity_lambda": 0.2,
    "filter": True,
    "generate_config": {
        "do_sample": True,
        "temperature": 0.2,
        "max_new_tokens": 512,
    }
}


from greaterprompt import (
    ApeOptimizer, ApoOptimizer, GreaterOptimizer, GreaterDataloader, Pe2Optimizer, TextGradOptimizer
)


greater_optimizer = GreaterOptimizer(
    model=model,
    tokenizer=tokenizer,
    optimize_config=greater_optimize_config # Optional
)

greater_result = greater_optimizer.optimize(
    dataset2,
    p_extractor="\nNext, only give the exact answer, no extract words or any punctuation:",
    rounds=2
)

print(f'greater_result: {greater_result}')
