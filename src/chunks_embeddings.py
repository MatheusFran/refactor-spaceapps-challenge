import os

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document



def split_documents(doc):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(doc)

    return md_header_splits


def embedding_documents(split_docs):
    embeddings_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        documents=split_docs,
        embedding=embeddings_model
    )

    return vectorstore


def save_vectorstores(vectorstore):
    save_path = '../data/vectordb'
    vectorstore.save_local(save_path)


if __name__ == "__main__":
    path_files = '../data/processed'
    all_documents = []

    for filename in os.listdir(path_files):
        if filename.endswith(".md"):
            file_path = os.path.join(path_files, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                doc_text = f.read()
                splits = split_documents(doc_text)
                for chunk_text in splits:
                    all_documents.append(
                        chunk_text
                    )

    vectorstore = embedding_documents(all_documents)
    save_vectorstores(vectorstore)