from langchain.tools.retriever import create_retriever_tool
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def retriever_tool():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_index_path = '../data/vectordb'

    vectordb = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    retriever_tool = create_retriever_tool(
        retriever,
        "retrieve_blog_posts",
        "Search and return information about Lilian Weng blog posts.",
    )

    return retriever_tool
