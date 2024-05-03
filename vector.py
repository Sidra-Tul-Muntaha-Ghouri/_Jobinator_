from key import KEY
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index.core import download_loader, StorageContext
import os
import openai
os.environ['OPENAI_API_KEY'] = KEY
def create_vector(dir):
    dirs = f"data_dir/{dir}"
    documents = SimpleDirectoryReader(dirs).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)

    storage_context = StorageContext.from_defaults()
    index.storage_context.persist(f"./vector/{dir}")
    print ("Done")

