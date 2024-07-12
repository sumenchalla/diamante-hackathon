from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
#from langchain_huggingface import HuggingFaceEmbeddings updated as version changed

#Loading the data
loader = PyPDFLoader("Data/diamante-net-whitepaper.pdf")
pages = loader.load_and_split()






documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)



db = Chroma.from_documents(documents, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
retriever = db.as_retriever(search_kwargs={"k": 2})




model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#llm = CTransformers(model="Fan21/Llama-mt-lora",model_type="llama",config={"temperature":0.5,'context_length' : 2048},device='cuda')

