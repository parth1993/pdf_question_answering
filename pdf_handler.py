from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load_and_split()
    # fetch content of each page
    document = "".join([doc.page_content for doc in documents])
    # split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)

    return texts