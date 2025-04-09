import flax.serialization
import os
import json
from huggingface_hub import hf_hub_download, create_repo, upload_file, login
import os
from .independent import debug_state
from ._utils import convert_tree
from .model import *


@debug_state.trace_func
def load_model(path,dtype= None):
    with open(os.path.join(path, "understanding_good_stuff.json"), "r") as f:
        data = json.load(f)
    
    model = ModelManager(data["num_heads"],data["attention_dim"],data["vocab_size"],data["num_blocks"],data["ff_dim"],data["dropout_rate"],dtype=dtype)
    with open(os.path.join(path, "good_stuff.pkl"), "rb") as f:
        model.params = convert_tree(dtype,flax.serialization.from_bytes(model.params, f.read()))
    return model

@debug_state.trace_func
def load_hf(path,dtype= None):
    model_repo = path
    filenames = ["understanding_good_stuff.json","good_stuff.pkl","make_stuff_better.pkl"]
    for i in filenames:
        try:
            print(hf_hub_download(repo_id=model_repo, filename=i,local_dir="Loaded_model"))
        except:
            print(f"No {i} found")
    return load_model("Loaded_model",dtype)

@debug_state.trace_func
def push_model(repo_name, folder_path):
    files_to_upload = ["good_stuff.pkl", "understanding_good_stuff.json","make_stuff_better.pkl"]
    
    create_repo(repo_name, exist_ok=True)  # Create repo if it doesn’t exist

    for file_name in files_to_upload:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Only upload if the file exists
            upload_file(
                path_or_fileobj=file_path,
                path_in_repo=file_name,  # Save with the same filename
                repo_id=repo_name,
                repo_type="model",
            )
    print(f"Uploaded {files_to_upload} to {repo_name}")