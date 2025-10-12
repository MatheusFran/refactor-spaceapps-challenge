from langchain.tools.retriever import create_retriever_tool


def retriever_tool():
    retriever_tool = create_retriever_tool(
        retriever,
        "retrieve_blog_posts",
        "Search and return information about Lilian Weng blog posts.",
    )

    return retriever_tool
