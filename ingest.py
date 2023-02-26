"""Load html from files, clean up, split, ingest into Weaviate."""
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def ingest_txt(file, as_text=False):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
        
    """Get documents from texts."""
    if type(file) == str :
        texts = text_splitter.split_text(file)
    else:
        loader = TextLoader(file)
        documents = loader.load()
        if len(documents) == 1:
            texts = text_splitter.split_text(documents[0].page_content)
        else: 
            pass #split documents


    def docs_from_list(texts, filename=None):
        documents = []
        for i, text in enumerate(texts):
            documents.append(Document(
                page_content=text,
                metadata={"source": f"{filename}"},))

        return documents

    docs = docs_from_list(texts)
    
    # global vectorstore
    # vectorstore = FAISS.from_documents(docs, embeddings)

    # https://langchain.readthedocs.io/en/latest/_modules/langchain/text_splitter.html#TextSplitter.create_documents
    # metadatas = metadatas or [{}] * len(texts)
    # documents = []
    # for i, text in enumerate(texts):
    #     for chunk in self.split_text(text):
    #         documents.append(Document(page_content=chunk, metadata=_metadatas[i]))
    # return documents
    
    return docs

