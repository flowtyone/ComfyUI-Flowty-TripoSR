from pathlib import Path

MODEL_CACHE_PATH = Path(__file__).parent.joinpath("models", "cache")

if not MODEL_CACHE_PATH.exists():
    try:
        MODEL_CACHE_PATH.mkdir(parents=True)
    except Exception:
        MODEL_CACHE_PATH = None
