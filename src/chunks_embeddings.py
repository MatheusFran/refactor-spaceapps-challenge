from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


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