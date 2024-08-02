import torch
import random
from exllamav2 import(
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
)

from exllamav2.generator import (
    ExLlamaV2BaseGenerator,
    ExLlamaV2Sampler
)
"""Run a single prediction on the model"""
def exllama_query(query):
    config = ExLlamaV2Config()
    config.model_dir = "."
    config.prepare()
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, lazy = True)
    model.load()
    tokenizer = ExLlamaV2Tokenizer(config)   
    # Initialize generator

    generator = ExLlamaV2BaseGenerator(model, cache, tokenizer)
    # Define settings

    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 1.10
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.15

    generator.warmup()
    print("generator warmed up")
    print("Inference Started")

    output = generator.generate_simple(query, settings, num_tokens= 512, seed = random.randint(0,10**20))
        
    print(output)
query = "What is the meaning of life?"
exllama_query(query)       