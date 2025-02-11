# Plan is to eventually put all this into a yaml config
QUERY_CONFIG = {
    # Note: Sigma shift value, publicly released models use 3.0
    "shift": 3.0,
    
    # Naturally, adjust to the width/height of the model you have
    "width": 1024,
    "height": 1024,
    
    # Pick your prompt
    "test_prompt": "a photo of a cat kneading dough",
    
    # Most models prefer the range of 4-5, but still work well around 7
    "cfg_scale": 4.5,
    
    # Different models want different step counts but most will be good at 50, albeit that's slow to run
    # sd3_medium is quite decent at 28 steps
    "steps": 40,
    
    # Seed
    "seed": 23,
    
    # Can be "roll", "fixed" or "rand"
    "seed_type": "rand",
    
    # Actual model file path
    # "model": "models/sd3_medium.safetensors"
    # "model": "models/sd3.5_large_turbo.safetensors"
    "model": "/data01/2project/sd3.5/models/sd3.5_medium.safetensors",
    
    # VAE model file path, or set None to use the same model file
    # "models/sd3_vae.safetensors",
    "vae_file": None,
    
    # Optional init image file path
    "init_image": None,
    
    # ControlNet
    "controlnet_cond_image": None,
    
    # If init_image is given, this is the percentage of denoising steps to run (1.0: full denoise, 0.0: no denoise at all)
    "denoise": 0.8,
    
    # SAMPLER
    "sampler": "dpmpp_2m",
    
    # MODEL FOLDER
    "model_folder": "/data01/2project/sd3.5/models",
    
    # Newly adding the following here as a config from what used to be main()'s parameters:
    # Postfix
    "postfix": None,
    
    "controlnet_ckpt": None,
    
    "require_skip_layer_config": False,
    
    "verbose": False,
    
    "text_encoder_device": "cpu",
}

MODEL_CONFIGS = {
    "sd3_medium": {
        "shift": 1.0,
        "steps": 50,
        "cfg": 5.0,
        "sampler": "dpmpp_2m",
    },
    "sd3.5_medium": {
        "shift": 3.0,
        "steps": 50,
        "cfg": 5.0,
        "sampler": "dpmpp_2m",
        "skip_layer_config": {
            "scale": 2.5,
            "start": 0.01,
            "end": 0.20,
            "layers": [7, 8, 9],
            "cfg": 4.0,
        },
    },
    "sd3.5_large": {
        "shift": 3.0,
        "steps": 40,
        "cfg": 4.5,
        "sampler": "dpmpp_2m",
    },
    "sd3.5_large_turbo": {"shift": 3.0, "cfg": 1.0, "steps": 4, "sampler": "euler"},
    "sd3.5_large_controlnet_blur": {
        "shift": 3.0,
        "steps": 60,
        "cfg": 3.5,
        "sampler": "euler",
    },
    "sd3.5_large_controlnet_canny": {
        "shift": 3.0,
        "steps": 60,
        "cfg": 3.5,
        "sampler": "euler",
    },
    "sd3.5_large_controlnet_depth": {
        "shift": 3.0,
        "steps": 60,
        "cfg": 3.5,
        "sampler": "euler",
    },
}

CLIPG_CONFIG = {
    "hidden_act": "gelu",
    "hidden_size": 1280,
    "intermediate_size": 5120,
    "num_attention_heads": 20,
    "num_hidden_layers": 32,
}

CLIPL_CONFIG = {
    "hidden_act": "quick_gelu",
    "hidden_size": 768,
    "intermediate_size": 3072,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
}

T5_CONFIG = {
    "d_ff": 10240,
    "d_model": 4096,
    "num_heads": 64,
    "num_layers": 24,
    "vocab_size": 32128,
}

CONTROLNET_MAP = {
    "time_text_embed.timestep_embedder.linear_1.bias": "t_embedder.mlp.0.bias",
    "time_text_embed.timestep_embedder.linear_1.weight": "t_embedder.mlp.0.weight",
    "time_text_embed.timestep_embedder.linear_2.bias": "t_embedder.mlp.2.bias",
    "time_text_embed.timestep_embedder.linear_2.weight": "t_embedder.mlp.2.weight",
    "pos_embed.proj.bias": "x_embedder.proj.bias",
    "pos_embed.proj.weight": "x_embedder.proj.weight",
    "time_text_embed.text_embedder.linear_1.bias": "y_embedder.mlp.0.bias",
    "time_text_embed.text_embedder.linear_1.weight": "y_embedder.mlp.0.weight",
    "time_text_embed.text_embedder.linear_2.bias": "y_embedder.mlp.2.bias",
    "time_text_embed.text_embedder.linear_2.weight": "y_embedder.mlp.2.weight",
}
