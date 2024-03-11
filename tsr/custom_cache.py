from pathlib import Path
from huggingface_hub import hf_hub_download

MODEL_CACHE_PATH = Path(__file__).parent.joinpath("models", "cache")

if not MODEL_CACHE_PATH.exists():
    try:
        MODEL_CACHE_PATH.mkdir(parents=True)
    except Exception:
        MODEL_CACHE_PATH = None


def custom_hf_download(repo_id, filename, cache_dir="", subfolder=""):
    """
    ref: https://github.com/Fannovel16/comfyui_controlnet_aux/pull/96/files
    """
    local_dir = Path(cache_dir).joinpath(repo_id)
    model_path = Path(local_dir).joinpath(subfolder, filename)
    if not model_path.exists():
        cache_dir_d = Path(cache_dir).joinpath(repo_id, "cache")
        model_path = hf_hub_download(repo_id=repo_id,
                                     cache_dir=cache_dir_d,
                                     local_dir=local_dir,
                                     subfolder=subfolder,
                                     filename=filename,
                                     local_dir_use_symlinks=False,
                                     resume_download=True,
                                     etag_timeout=100,
                                     )
        try:
            import shutil
            shutil.rmtree(cache_dir_d)
        except Exception as e:
            print(e)
    return model_path
