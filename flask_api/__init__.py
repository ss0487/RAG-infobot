# enable GPU: https://docs.haystack.deepset.ai/docs/enabling-gpu-acceleration
# importing completed pipeline from pipeline.py
import os
from flask import Flask, request
from markupsafe import escape
from document_pipeline import indexing_pipeline
from inference_pipeline import rag_inf_pipeline
from document_store import pgvector_store
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime
import os

print("__name__: " + __name__, "\n")
print(os.getcwd() + "\n")

def create_app(test_config=None):
    
    print("PYTHONPATH: " + str(os.getenv("PYTHONPATH")) + "\n")
    
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
    
    output_dir = app.root_path + "/static/data"
    sources = list(Path(output_dir).glob("**/*"))
    print("Number of available files: " + str(len(sources)) + "\n")

    if len(sources):
        # Run the doc pipeline
        doc_pipeline_start = datetime.datetime.now()
        print("Document pipeline start time: " + doc_pipeline_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        
        num_docs = indexing_pipeline.run({
            "converter": {
                "sources": sources
            }
        })
        
        doc_pipeline_end = datetime.datetime.now()
        print("Document pipeline end time: " + doc_pipeline_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        
        duration = doc_pipeline_end - doc_pipeline_start
        
        print("Time taken to run document pipeline: " + str(duration.seconds) + " seconds\n")

        print("Number of documents in the document store: " + str(pgvector_store.count_documents()) + "\n")
    
    else:
        # Just run the LLM without documents
        print("No documents loaded, so falling back to plain LLM calls.\n")
    
    # Warm up the inference pipeline
    print("Warming up the inference pipeline.\nWarm-up query:")
    inference_pipeline = rag_inf_pipeline
    warm_up_query = "This is a dummy query to warm up the pipeline."
    print(warm_up_query + "\n")
    
    inf_pipeline_warmup_start = datetime.datetime.now()
    print("Inference pipeline warm-up start time: " + inf_pipeline_warmup_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    warm_up_resp = inference_pipeline.run({
        "text_embedder": {
            "text": warm_up_query
        },
        "prompt_builder": {
            "question": warm_up_query
        },
    })
    
    inf_pipeline_warmup_end = datetime.datetime.now()
    print("Inference pipeline warm-up end time: " + inf_pipeline_warmup_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    warm_up_duration = inf_pipeline_warmup_end - inf_pipeline_warmup_start
    
    print("Time taken to warm-up inference pipeline: " + str(warm_up_duration.seconds) + " seconds\n")
    print("Pipeline response to warm-up:")
    print(warm_up_resp["llm"]["replies"][0] + "\n")
    
    @app.route("/generate", methods=['POST', 'GET'])
    def haystack_qa():
        if request.method == 'POST':
            print("DEBUG:\nRequest data:\n" + str(request.form.keys()) + "\n")
            
            # Asking a Question
            question = request.form.get('question', '')
            
            if question == '':
                return "Please enter a question."
           
            print("About to generate text in response to the following question:")
            inf_pipeline_start = datetime.datetime.now()
            print("Inference pipeline start time: " + inf_pipeline_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            print(question + "\n")
            
            res = inference_pipeline.run({
                "text_embedder": {
                    "text": question
                },
                "prompt_builder": {
                    "question": question
                },
            })
            answers = res["llm"]["replies"]
            
            if answers:
                # Return the first answer
                # return "\n\nResult:\n" + answers[0] + "\n\n---------------END OF RESPONSE----------------\n\n"
                inf_pipeline_end = datetime.datetime.now()
                print("Inference pipeline end time: " + inf_pipeline_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                inf_duration = inf_pipeline_end - inf_pipeline_start
                print("Time taken for inference: " + str(inf_duration.seconds) + " seconds\n")
                print("Pipeline response: " + answers[0] + "\n")
                return answers[0]
            print("No response")
            return "**No response**"
        else:
            return "Bad request. Please make a POST request and not a GET request."

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            files = request.files
            print(files.items())
            # for filename, filecontent in files.items():
            #     filecontent.save(output_dir + "/" + secure_filename(filename))
            return "Files received!"
    return app