import os
import glob
from dotenv import load_dotenv
import gradio as gr
from pypdf import PdfReader
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def readpdf(cvfile):
    response_text = ""
    reader = PdfReader(cvfile)
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        response_text += text
    return response_text

def readtxt(cvfile):
    response_text = ""
    with open(cvfile, 'r', encoding="utf-8") as file:
        cvcontent = file.read()
        response_text = cvcontent
    return response_text

MODEL = "gpt-4o-mini"


load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')

cvdir = "cvdocs/"
files = os.listdir(cvdir)

class cvclass:
  def __init__(self, page_content, metadata):
    self.page_content = page_content
    self.metadata = metadata
      
documents = []
for cvfile in files:
    cvcontent = ""
    doctype = "unknown"
    if cvfile.endswith('.txt'):
        cvcontent=readtxt(cvdir + cvfile)
        doctype = "txt"
    if cvfile.endswith('.pdf'):
        cvcontent=readpdf(cvdir + cvfile)
        doctype = "pdf"
    metadata = dict(source = cvdir + cvfile, doc_type = cvfile[:-4])
    page_content = cvcontent
    cv = cvclass(cvcontent, metadata)
    documents.append(cv)
    #print(cv.metadata)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

#print(f"Total number of chunks: {len(chunks)}")

embeddings = OpenAIEmbeddings()
db_name = "vector_db"
if os.path.exists(db_name):
    Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
print(f"Vectorstore created with {vectorstore._collection.count()} documents")

collection = vectorstore._collection
count = collection.count()

sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
dimensions = len(sample_embedding)
print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")

llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
retriever = vectorstore.as_retriever(search_kwargs={"k": 25})

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)

def chat(question, history):
    result = conversation_chain.invoke({"question": question})
    return result["answer"]

view = gr.ChatInterface(chat, type="messages").launch()
