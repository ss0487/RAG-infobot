# configure model for generating the answers

from getpass import getpass
from haystack.components.generators import HuggingFaceLocalGenerator
import torch

model_settings = {
        "model_name": "meta-llama/Llama-3.1-8B-Instruct",
        "device_map": "auto",
        "torch_dtype": torch.bfloat16,
        "device": "cuda",
        "load_in_4bit": True,
}
   
llama_generator = HuggingFaceLocalGenerator(model=model_settings["model_name"],
                                      huggingface_pipeline_kwargs={
                                        "device_map": model_settings["device_map"],
                                        "model_kwargs": {
                                            "load_in_4bit": model_settings["load_in_4bit"],
                                            "bnb_4bit_use_double_quant": True,
                                            "bnb_4bit_quant_type": "nf4",
                                            "bnb_4bit_compute_dtype": model_settings["torch_dtype"],
                                        }
                                      },
                                      generation_kwargs={
                                        "max_new_tokens": 256,
                                        "temperature": 0.9,
                                      })