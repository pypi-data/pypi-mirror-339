from sentence_transformers import SentenceTransformer

from .prompts import *
from .quick_rag import *
from .smart_llm import *
from .text_splitter import *
from .web_tools import *

model_name = "all-MiniLM-L6-v2"

try:
    SentenceTransformer(model_name)
except Exception:
    print("Retrying to download: ",{model_name})
    SentenceTransformer(model_name)