import os
import json
import fitz
from chromadb.utils import embedding_functions

ssd_path = "/Volumes/YOUR_SSD_NAME/YOUR_FOLDER/"

db_path = "./chroma_db"

# Tell about in how many chunks will the data be divided into

chunk_size = 500

#

chunk_overlap = 50

def split_chunk(text: str, filename: str, page_num: int) -> list:
    chunks = []
    start = 0