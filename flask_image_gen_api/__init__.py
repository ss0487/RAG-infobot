import torch
from inference_components.sd3_infer import SD3Inferencer
from config.config import QUERY_CONFIG, MODEL_CONFIGS
from flask import Flask, request
from markupsafe import escape
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import re
import os
import datetime

@torch.no_grad()
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    
    print("\nApp root path: " + app.root_path + "\n")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    # load configs for chosen model
    chosen_model = QUERY_CONFIG.get("model")
    model_name = os.path.splitext(os.path.basename(chosen_model))[0]
    chosen_model_config = MODEL_CONFIGS.get(model_name, {})
    _shift = chosen_model_config.get("shift", 3)
    _steps = chosen_model_config.get("steps", 50)
    _cfg = chosen_model_config.get("cfg", 5)
    _sampler = chosen_model_config.get("sampler", "dpmpp_2m")
    
    out_dir = os.getenv("OUTPUT_DIRECTORY")
    postfix = QUERY_CONFIG.get("postfix")
    seed = QUERY_CONFIG.get("seed")
    seed_type = QUERY_CONFIG.get("seed_type")
    width = QUERY_CONFIG.get("width")
    height = QUERY_CONFIG.get("height")
    controlnet_ckpt = QUERY_CONFIG.get("controlnet_ckpt")
    controlnet_cond_image = QUERY_CONFIG.get("controlnet_cond_image")
    vae = QUERY_CONFIG.get("vae_file")
    init_image = QUERY_CONFIG.get("init_image")
    denoise = QUERY_CONFIG.get("denoise")
    require_skip_layer_config = QUERY_CONFIG.get("require_skip_layer_config")
    verbose = QUERY_CONFIG.get("verbose")
    model_folder = QUERY_CONFIG.get("model_folder")
    text_encoder_device = QUERY_CONFIG.get("text_encoder_device")    

    if require_skip_layer_config:
        skip_layer_config = chosen_model_config.get("skip_layer_config", {})
        cfg = skip_layer_config.get("cfg", cfg)
    else:
        skip_layer_config = {}

    if controlnet_ckpt is not None:
        controlnet_config = CONFIGS.get(
            os.path.splitext(os.path.basename(controlnet_ckpt))[0], {}
        )
        _shift = controlnet_config.get("shift", shift)
        _steps = controlnet_config.get("steps", steps)
        _cfg = controlnet_config.get("cfg", cfg)
        _sampler = controlnet_config.get("sampler", sampler)

    inferencer = SD3Inferencer()
    
    # Load inferencer with model
    print("Loading the inferencer...\n")
    
    inferencer_load_start = datetime.datetime.now()
    print("Inferencer load start time: " + inferencer_load_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")

    inferencer.load(
        chosen_model,
        vae,
        _shift,
        model_folder,
        controlnet_ckpt,
        text_encoder_device,
        verbose,
    )
    
    print("Loaded the inferencer.\n")

    inferencer_load_end = datetime.datetime.now()
    print("Inferencer load end time: " + inferencer_load_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    load_duration = inferencer_load_end - inferencer_load_start
    print("Time taken to load inferencer: " + str(load_duration.seconds) + " seconds\n")

    test_prompt = QUERY_CONFIG.get("test_prompt")
    print("Test prompt:\n" + test_prompt + "\n")
    
    print("Creating the output directory...\n")
    sanitized_prompt = re.sub(r"[^\w\-\.]", "_", test_prompt)
    out_path = os.path.join(
        out_dir,
        (
            model_name
            + (
                "_" + os.path.splitext(os.path.basename(controlnet_ckpt))[0]
                if controlnet_ckpt is not None
                else ""
            )
        ),
        # Limit the filename part to 30 chars plus timestamp
        os.path.splitext(os.path.basename(sanitized_prompt))[0][:30]
        + (postfix or datetime.datetime.now().strftime("_%Y-%m-%dT%H-%M-%S")),
    )

    os.makedirs(out_path, exist_ok=False)
    print("...done creating output directory.\n")
    
    inferencer_test_start = datetime.datetime.now()
    print("Inferencer test start time: " + inferencer_test_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    test_out_img_save_path = inferencer.gen_image(
        [test_prompt],
        width,
        height,
        _steps,
        _cfg,
        _sampler,
        seed,
        seed_type,
        out_path,
        controlnet_cond_image,
        init_image,
        denoise,
        skip_layer_config,
    )

    inferencer_test_end = datetime.datetime.now()
    print("Inferencer test end time: " + inferencer_test_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")

    test_duration = inferencer_test_end - inferencer_test_start
    print("Time taken to test inferencer: " + str(test_duration.seconds) + " seconds\n")

    print("Test image stored in " + test_out_img_save_path + "\n")

    @app.route("/generate-image", methods=['POST', 'GET'])
    def stableDiffImageGen():
        if request.method == 'POST':
            print("DEBUG:\nRequest data:\n" + str(request.form.keys()) + "\n")
            
            # Getting the prompt from the streamlit request
            prompt = request.form.get('prompt', '')
            
            if prompt == '':
                return "Please enter a prompt."

            print("Creating the output directory...\n")
            sanitized_prompt = re.sub(r"[^\w\-\.]", "_", prompt)
            out_path = os.path.join(
                out_dir,
                (
                    model_name
                    + (
                        "_" + os.path.splitext(os.path.basename(controlnet_ckpt))[0]
                        if controlnet_ckpt is not None
                        else ""
                    )
                ),
                # Limit the filename part to 30 chars plus timestamp
                os.path.splitext(os.path.basename(sanitized_prompt))[0][:30]
                + (postfix or datetime.datetime.now().strftime("_%Y-%m-%dT%H-%M-%S")),
            )

            os.makedirs(out_path, exist_ok=False)
            print("...done creating output directory.\n")

            print("About to generate an image in response to the following prompt:")
            print(prompt + "\n")
            inf_start = datetime.datetime.now()
            print("Inference start time: " + inf_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            
            out_img_save_path = inferencer.gen_image(
                [prompt],
                width,
                height,
                _steps,
                _cfg,
                _sampler,
                seed,
                seed_type,
                out_path,
                controlnet_cond_image,
                init_image,
                denoise,
                skip_layer_config,
            )
            
            inf_end = datetime.datetime.now()
            print("Inference end time: " + inf_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            inf_duration = inf_end - inf_start
            print("Time taken for inference: " + str(inf_duration.seconds) + " seconds\n")
            print("Image path: " + out_img_save_path + "\n")
            return {"response_type": "image", "image_path": out_img_save_path}
            
            print("No response")
            return "**No response**"
        else:
            return "Bad request. Please make a POST request and not a GET request."
    return app